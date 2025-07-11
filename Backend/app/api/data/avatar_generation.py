import asyncio
import base64
from typing import List, Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from os import getenv
from openai import OpenAI

from ...core.application import AddRouter
from ...core.security.decorators import secured_endpoint
from ...db.postgress.engine import getSession
from ...core.config import Config

# Initialize OpenAI client
try:
    openai_config = Config.get_property(None, "openai", ["base_url"])
    openai_client = OpenAI(
        api_key=getenv("OPENAI_API_KEY","none"),
        base_url=openai_config.get("base_url")  # Optional: for Azure or custom endpoints
    )
    image_settings = Config.get_property(None, "openai", ["image_generation"])
except Exception as e:
    print(f"Warning: OpenAI client initialization failed: {e}")
    openai_client = None

# Pydantic Models
class AvatarGenerationRequest(BaseModel):
    """Request model for avatar generation"""
    gender: str = Field(..., description="Avatar gender: 'boy', 'girl', or 'neutral'")
    skinColor: Optional[str] = Field(None, description="Avatar skin color: 'claire', 'moyenne claire', 'moyenne', 'moyenne foncée', or 'foncée'")
    accessories: Optional[str] = Field(None, description="Comma-separated accessories or 'none'")
    color: Optional[str] = Field(None, description="Preferred color")
    passions: Optional[List[str]] = Field(None, description="List of user's passions/interests")
    expression: Optional[str] = Field(None, description="Avatar expression")

class AvatarData(BaseModel):
    """Individual avatar data"""
    id: str = Field(..., description="Unique identifier for this avatar")
    data_url: str = Field(..., description="Base64 data URL of the image")
    prompt_variation: str = Field(..., description="The specific prompt used for this variation")
    revised_prompt: Optional[str] = Field(None, description="The AI-revised prompt (if available)")

class AvatarGenerationResponse(BaseModel):
    """Response model for avatar generation"""
    avatars: List[AvatarData] = Field(..., description="List of generated avatars")
    message: str = Field("Avatars generated successfully", description="Response message")
    generation_time: float = Field(..., description="Total generation time in seconds")

# Router
avatar_router = APIRouter(prefix="/avatars", tags=["Avatar Generation"])

def build_avatar_prompt(gender: str, skinColor: Optional[str] = None, accessories: Optional[str] = None, 
                       color: Optional[str] = None, passions: Optional[List[str]] = None, 
                       expression: Optional[str] = None, variation_suffix: str = "") -> str:
    """
    Build the avatar generation prompt based on user preferences.
    
    Args:
        gender: Avatar gender ('boy', 'girl', 'neutral')
        skinColor: Avatar skin color ('claire', 'moyenne claire', 'moyenne', 'moyenne foncée', 'foncée')
        accessories: Accessories string
        color: Preferred color
        passions: List of user's passions/interests
        expression: Avatar expression
        variation_suffix: Additional text to create variation
        
    Returns:
        Complete prompt string for image generation
    """
    # Convert gender to French
    gender_fr = {
        'boy': 'masculin',
        'girl': 'féminin', 
        'neutral': 'neutre'
    }.get(gender, 'neutre')
    
    # Build skin color text
    skin_color_text = ""
    if skinColor:
        skin_color_text = f"avec une peau de couleur {skinColor}"
    
    # Build accessories text
    accessories_text = "sans accessoires particuliers"
    if accessories and accessories != 'none':
        accessories_list = [acc.strip() for acc in accessories.split(',')]
        accessories_text = f"portant les accessoires suivants : {', '.join(accessories_list)}"
    
    # Build color text
    color_text = ""
    if color:
        color_text = f"avec des tons dominants de {color}"
    
    # Build passions text
    passions_text = ""
    if passions and len(passions) > 0:
        if len(passions) == 1:
            passions_text = f"reflétant la passion pour {passions[0]}"
        else:
            passions_text = f"reflétant la passion pour {', '.join(passions[:-1])} et {passions[-1]}"

    # Build expression text
    expression_text = ""
    if expression:
        expression_text = f"avec une expression {expression}"
    
    # Base prompt (preserved from frontend)
    base_prompt = f"""
Créer une illustration numérique en style cartoon réaliste 2D, traits doux,
palette de couleurs naturelle et harmonieuse, rendu propre et professionnel.

Fond : blanc uni pur (#FFFFFF), sans motif, sans dégradé, sans ombre.
Aucun objet, décor, texte ou palette de couleurs autour du personnage.

Personnage : de genre {gender_fr}, {skin_color_text}, {accessories_text}, {color_text}, {passions_text}, {expression_text}.
Vue de face, position debout, le modèle est coupé à la taille, au niveau de la ceinture, proportions naturelles,
cadré et centré dans l'image, bien éclairé, détails soignés sur vêtements et accessoires.
ne coupez jamais la tête de la personne sur la photo.

Objectif : obtenir un avatar haut de gamme, isolé sur fond blanc, prêt pour un détourage automatique et une utilisation professionnelle ou commerciale.
{variation_suffix}
""".strip()
    
    return base_prompt

async def generate_single_avatar(prompt: str, avatar_id: str) -> Dict[str, Any]:
    """
    Generate a single avatar using OpenAI's Responses API with image generation tool.
    
    Args:
        prompt: The image generation prompt
        avatar_id: Unique identifier for this avatar
        
    Returns:
        Dictionary containing avatar data or error information
    """
    if not openai_client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OpenAI client not initialized"
        )
    
    try:
        # Use the new Responses API with image generation tool
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: openai_client.responses.create(
                model="gpt-4.1-mini",  # Use a supported language model
                input=prompt,
                tools=[{
                    "type": "image_generation",
                    "size": image_settings.get("size", "1024x1024"),  # Default size if not specified
                    "quality": image_settings.get("quality", "low"),  # Default quality
                    "output_format": image_settings.get("format", "jpeg"),
                    # "background" : image_settings.get("background", "transparent")  # Default format

                }]
            )
        )
        
        # Extract image data from the response
        image_data = [
            output.result
            for output in response.output
            if output.type == "image_generation_call"
        ]
        
        if not image_data:
            raise Exception("No image generated in response")
        
        # Get the base64 image data
        image_b64 = image_data[0]
        
        # Create data URL
        data_url = f"data:image/png;base64,{image_b64}"
        
        # Extract revised prompt if available
        revised_prompt = prompt  # Default to original
        for output in response.output:
            if output.type == "image_generation_call" and hasattr(output, 'revised_prompt'):
                revised_prompt = output.revised_prompt
                break
        
        return {
            "success": True,
            "data": {
                "id": avatar_id,
                "data_url": data_url,
                "prompt_variation": prompt,
                "revised_prompt": revised_prompt
            }
        }
        
    except Exception as e:
        print(f"Error generating avatar {avatar_id}: {e}")
        return {
            "success": False,
            "error": str(e),
            "avatar_id": avatar_id
        }

@avatar_router.post("/generate", response_model=AvatarGenerationResponse)
@secured_endpoint()
async def generate_avatars(
    request: AvatarGenerationRequest,
    jwt: dict,
):
    """
    Generate 3 avatar variations based on user preferences.
    
    Requires authentication via access token.
    """
    import time
    start_time = time.time()
    
    user_id = jwt["sub"]
    
    try:
        # Create 3 prompt variations for diversity
        prompt_variations = [
            ("avatar_1", "Style légèrement plus doux et arrondi."),
            ("avatar_2", "Avec des détails légèrement plus fins et précis."), 
            ("avatar_3", "Couleurs légèrement plus vives et contrastées.")
        ]
        
        # Build base prompts with variations
        generation_tasks = []
        for avatar_id, variation in prompt_variations:
            full_prompt = build_avatar_prompt(
                gender=request.gender,
                skinColor=request.skinColor,
                accessories=request.accessories,
                color=request.color,
                passions=request.passions,
                expression=request.expression,
                variation_suffix=variation
            )
            
            # Create async task for each generation
            task = generate_single_avatar(full_prompt, avatar_id)
            generation_tasks.append(task)
        
        # Generate all 3 avatars concurrently (with some delay to avoid rate limits)
        results = []
        for i, task in enumerate(generation_tasks):
            if i > 0:
                # Add small delay between requests to avoid rate limiting
                await asyncio.sleep(1)
            
            result = await task
            results.append(result)
        
        # Process results
        successful_avatars = []
        failed_generations = []
        
        for result in results:
            if result["success"]:
                successful_avatars.append(AvatarData(**result["data"]))
            else:
                failed_generations.append({
                    "avatar_id": result["avatar_id"],
                    "error": result["error"]
                })
        
        # Check if we have at least one successful generation
        if not successful_avatars:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate any avatars. Errors: {failed_generations}"
            )
        
        # Log any partial failures
        if failed_generations:
            print(f"Some avatar generations failed for user {user_id}: {failed_generations}")
        
        generation_time = time.time() - start_time
        
        return AvatarGenerationResponse(
            avatars=successful_avatars,
            message=f"Generated {len(successful_avatars)}/3 avatars successfully",
            generation_time=round(generation_time, 2)
        )
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"Unexpected error generating avatars for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during avatar generation"
        )

@avatar_router.get("/test-connection")
@secured_endpoint()
async def test_openai_connection(jwt: dict):
    """
    Test endpoint to verify OpenAI connection and image generation capability.
    """
    if not openai_client:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OpenAI client not initialized"
        )
    
    try:
        # Test with a simple image generation call using the new API
        test_response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: openai_client.responses.create(
                model="gpt-4.1-mini",
                input="Generate a simple test image of a blue circle",
                tools=[{
                    "type": "image_generation",
                    "size": "1024x1024",
                    "quality": "low"  # Use low quality for testing
                }]
            )
        )
        
        # Check if image was generated
        image_data = [
            output.result
            for output in test_response.output
            if output.type == "image_generation_call"
        ]
        
        if image_data:
            return {
                "status": "success",
                "message": "OpenAI Responses API connection successful",
                "model": "gpt-4.1-mini with image_generation tool",
                "image_generated": True
            }
        else:
            return {
                "status": "partial_success",
                "message": "Connection successful but no image generated",
                "model": "gpt-4.1-mini with image_generation tool",
                "image_generated": False
            }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OpenAI connection failed: {str(e)}"
        )

# Add router to the application
AddRouter(avatar_router)
