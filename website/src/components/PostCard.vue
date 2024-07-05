<script setup>
    import { ref, defineProps } from 'vue'

    const props = defineProps(['post'])
    const content = props.post.content.substring(0, 150) + '...'

    const date = props.post.createdAt.substring(0, 10)
    const nbReplies = ref(props.post.replies.length)
</script>

<template>
    <div class="card">
        <div class="cardContent">
            <h1>{{ props.post.title }}</h1>
            <p>{{ content }}</p>
        </div>
        <div class="author">
            <p>{{ props.post.authorId }}</p>
        </div>
        <div class="stats">
            <p>{{ props.post.likes }}</p>
            <p>{{ nbReplies }}</p>
            <p>{{ date }}</p>
        </div>
    </div>
</template>

<style scoped>
    .card {
        display: flex;
        flex-direction: row;
        justify-content: start;
        align-items: center;
        border: 1px solid black;
        padding: 5px;

    }

    .cardContent {
        padding: 10px;
        min-width: 300px;
        width: 50%;
    }

    .author {
        display: flex;
        justify-content: center;
        width: 10%;
    }

    .stats {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: 30%;
        width: 10%;
    }

    .card h1 {
        font-size: 22px;
    }

    .card p {
        font-size: 15px;
    }
</style>

