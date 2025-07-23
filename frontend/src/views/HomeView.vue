<template>
  <div>
    <NavBar />
    <Carousel />
    <!-- <HeroSection /> -->
    <FeatureSection />
    <LatestVideos />
    <DownloadSection />
    
  </div>
</template>

<script setup lang="ts">
import NavBar from '../components/NavBar.vue'
import Carousel from '../components/Carousel.vue'
// import HeroSection from '../components/HeroSection.vue'
import LatestVideos from '../components/LatestVideos.vue'
import FeatureSection from '../components/FeatureSection.vue'
import DownloadSection from '../components/DownloadSection.vue'
</script>

<style scoped>
</style>
