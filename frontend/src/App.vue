<template>
		<AppHeader />
		<WebcamApp />
</template>

<script>
	import AppHeader from "./components/AppHeader.vue";
	import WebcamApp from "./components/WebcamApp.vue";

	export default {
		name: "App",
		components: {
			WebcamApp,
			AppHeader
		},
	};
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
  body {
    margin: 0;
    padding: 0;
    background-color: black;
  }
	#app {
		font-family: Roboto, Helvetica, Arial, sans-serif;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		text-align: center;
		color: white;
    @media (min-width: 1024px) {
      max-width: 70%;
      margin: 0 auto;
    }
	}
</style>
