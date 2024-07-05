<script setup>
    import { computed, defineProps } from 'vue'

    const props = defineProps(['category'])

    const iconClass = computed(() => {
        return `mdi ${props.category.iconName}`
    })

    const iconStyle = computed(() => {
        return {
            fontSize: '70px',
            color: props.category.color,
        }
    })
</script>

<template>
    <div class="card">
        <div class="icon">
            <i :class="iconClass" :style="iconStyle"></i>
        </div>
        <div class="text">
            <h1 class="title">{{ props.category.name }}</h1>
            <p class="description">{{ props.category.description }}</p>
        </div>
        <div class="topMessage">
            <ul>
                <li>Coucou un petit topic</li>
                <li>Un autre topic</li>
                <li>Ici ça parle heinnn</li>
            </ul>
        </div>
    </div>
</template>

<style scoped>
    .card {
        display: flex;
        flex-direction: row;
        justify-content: start;
        align-items: center;
    }

    .icon {
        margin-left: 10px;
    }

    .text {
        width: 50%;
        min-width: 150px;
        margin: 0 15px;
    }

    .title {
        font-size: 20px;
        margin-bottom: 0;
    }

    .description {
        font-size: 15px;
        margin-top: 5px;
    }

    .topMessage {
        margin-right: 10px;
    }
</style>

