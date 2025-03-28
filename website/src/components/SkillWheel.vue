<script setup>
    import { ref } from "vue";

    const segments = ref([
      "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"
    ]);

    const filled = ref([
        250, 410, 315, 285, 270, 265, 260, 256, 254 // I ajust 250 because there is no mathematical way to fix some gaps
    ]);

    const rotation = ref(0);
    const spinning = ref(false);
    const result = ref(null);

    const spinWheel = () => {
        if (spinning.value) {
            return;
        }
        spinning.value = true;
        const extraRotations = Math.floor(Math.random() * 3 + 3) * 360;
        const randomAngle = Math.floor(Math.random() * 360);

        rotation.value += extraRotations + randomAngle;
    
        setTimeout(() => {
            spinning.value = false;
            let normalizedAngle = rotation.value % 360;
            const segmentSize = 360 / segments.value.length;
            let segmentIndex = Math.round((360 - normalizedAngle) / segmentSize);
            if (segmentIndex === segments.value.length) {
                segmentIndex = 0;
            }
            result.value = segments.value[segmentIndex];
        }, 3000); 

    };

    const getSegmentStyle = (index) => {
        const angle = (360 / segments.value.length) * index;
        let height = (2 * Math.PI * filled.value[segments.value.length - 2]) / segments.value.length; 

        if (segments.value.length > 10) {
            height = (2 * Math.PI * 250) / segments.value.length; // 250 is the radius of the wheel (500px), 
        }

        if (segments.value.length === 2) {
            return {
                height: `${height}px`,
                transform: `rotate(${angle}deg)`,
                backgroundColor: `hsl(${angle}, 80%, 50%)`,
                clipPath: "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)",
            };
        }

        return {
            height: `${height}px`,
            transform: `rotate(${angle}deg)`,
            backgroundColor: `hsl(${angle}, 80%, 50%)`,
        };
    };
</script>

<template>
    <div class="wheel-container">
        <div class="wheel" :style="{ transform: `rotate(${rotation}deg)` }">
            <div class="segment"
                v-for="(segment, index) in segments" 
                :key="index" 
                :style="getSegmentStyle(index)"
            >
                <span class="segment-text">{{ segment }}</span>
            </div>
        </div>
        <div class="arrow">
        </div>
    </div>
        <button @click="spinWheel" :disabled="spinning">Spin</button>
        <p>{{ result }}</p>
</template>

<style scoped>
    .wheel-container {
        margin-top: 50px;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        transform: rotate(90deg);
    }

    .arrow {
        position: relative;
        top: -272px;
        left: -233px;
        width: 25px;
        height: 25px;
        background-color: rgb(255, 81, 0);
        clip-path: polygon(0% 0%, 100% 50%, 0% 100%);
    }

    .wheel {
        position: relative;
        width: 500px;
        height: 500px;
        border-radius: 50%;
        border: 5px solid #000;
        overflow: hidden;
        transition: transform 3s ease-out;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .segment {
        background-color: #007bff;
        clip-path: polygon(0% 0%, 100% 50%, 0% 100%);
        position: absolute;
        left: 0;
        transform-origin: center right;
        width: 50%;   
    }

    .segment-text {
        position: absolute;
        top: 50%;
        left: 20%;
        font-size: 20px;
        color: white;
        text-align: center;
    }

    button {
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        background: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        transition: 0.3s;
    }

    button:disabled {
        background: #aaa;
        cursor: not-allowed;
    }
</style>
