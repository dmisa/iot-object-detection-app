<template>
    <div class="hero-intro">
        <h1>Your AI-Powered Object Identification App</h1>
        <p>It is designed to run solely on a Raspberry Pi</p>
    </div>
</template>


<script>
    export default {
    name: "HeroIntro",
    mounted() {
    },
    methods: {
    },
    };
</script>

<style scoped>
    .hero-intro {
        text-align: center;
        color: white;
        font-family: 'Roboto', sans-serif;
        padding: 2rem;
    }

    h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    p {
        font-size: 1.2rem;
        color: #9A9D9E;
    }
</style>