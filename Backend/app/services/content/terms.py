"""
Initialize the first version of the Terms and Conditions in the database.
Run this script manually after your models are set up.
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database.postgress.config import getSession
from database.postgress.actions.terms_agreements import create_terms_version

# Sample Terms and Conditions content for the first version
INITIAL_TERMS_CONTENT = """
# Terms and Conditions

## 1. Introduction

Welcome to Autrement Capable! These Terms and Conditions govern your use of our platform.

## 2. Acceptance of Terms

By accessing or using Autrement Capable, you agree to be bound by these Terms and Conditions.

## 3. User Accounts

When you create an account with us, you must provide accurate information.

## 4. Privacy Policy

Your privacy is important to us. Please refer to our Privacy Policy for information on how we collect and use your data.

## 5. User Content

You are responsible for all content you provide to the platform.

## 6. Termination

We reserve the right to terminate your access to the platform for violations of these terms.

## 7. Changes to Terms

We may modify these terms at any time. Your continued use of the platform constitutes acceptance of the updated terms.

## 8. Contact Information

If you have any questions about these Terms, please contact us.
"""

async def init_terms():
    """Initialize the first version of the Terms and Conditions."""
    session = await getSession()
    try:
        # Create first version
        terms = await create_terms_version(
            session, 
            version="v1.0", 
            content=INITIAL_TERMS_CONTENT,
            is_active=True
        )
        if terms:
            print(f"Terms created: Version {terms.version}")
        else:
            print("Failed to create terms")
    finally:
        await session.close()

