<template>
    <div v-if="visible" class="overlay">
        <div class="popup-box">
            <span class="close-button" @click="closePopup">×</span>
            <img v-if="image" :src="image" alt="Popup Image" class="popup-image"/>
            <p>{{ message }}</p>
            <div class="buttons">
                <button @click="confirmAction">{{ buttonConfirm }}</button>
                <button @click="cancelAction">{{ buttonCancel }}</button>
            </div>
        </div>
    </div>
</template>
  
<script setup>
    import { defineProps, defineEmits } from 'vue'; 
    
    const props = defineProps({
        message: {
            type: String,
            default: 'Default popup message'
        },
        image: {
            type: String,
            default: ''
        }, 
        redirect: {
            type: String,
            default: '/'
        },
        buttonConfirm: {
            type: String,
            default: 'Default Yes'
        },
        buttonCancel: {
            type: String,
            default: 'Default No'
        },
        visible: {
            type: Boolean,
            default: true
        }
    });

    const emit = defineEmits(['close']);
  
    function confirmAction() {
        window.location.href = props.redirect;
    }
  
    function cancelAction() {
        emit('close');
    }

    function closePopup() {
        emit('close'); 
    }
</script>
  
<style scoped>
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 999;
    }
  
    .popup-box {
        background-color: white;
        padding: 2rem;
        width: 30%;
        height: 40%;
        border-radius: 1rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }

    .close-button {
        position: relative;
        top: -1rem;
        left: 51%;
        font-size: 2.5rem;
        font-weight: bold;
        color: #9c9c9c;
        cursor: pointer;
        transition: color 0.2s ease;
        background-color: transparent;
    }

    .close-button:hover {
        color: #333333;
        background-color: transparent;
    }
  
    .popup-image {
        max-width: 40%;
        height: auto;
    }

    .popup-box p {
        font-size: 1.2rem;
    }
  
    .buttons {
        display: flex;
        gap: 2rem;
        margin-top: 1rem;
    }

    button {
        padding: 0.6rem 1.2rem;
        border: none;
        border-radius: 0.75rem;
        background-color: #007bff;
        color: white;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }

    button:hover {
        background-color: #0056b3;
    }
  
</style>
  