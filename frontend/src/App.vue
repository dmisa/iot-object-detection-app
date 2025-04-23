<template>
		<AppHeader />
        <HeroIntro />
		<WebcamApp />
</template>

<script>
	import AppHeader from "./components/header/AppHeader.vue";
	import WebcamApp from "./components/webcam/WebcamApp.vue";
    import HeroIntro from "./components/hero/HeroIntro.vue";

	export default {
		name: "App",
		components: {
			WebcamApp,
			AppHeader,
            HeroIntro
		},
	};
</script>