<!-- src/views/HomeView.vue -->
<template>
  <div>
    
    <Carousel />
    <div class="bg-beige w-full">
      <div class="max-w-7xl mx-auto px-4 py-10 grid md:grid-cols-2 gap-3 pt-3 pb-3">
        <EventStatsCarousel />
        <HomeVideoPreview />
      </div>
    </div>
    <!-- <HeroSection /> -->
    <FeatureSection />
    <!-- <LatestVideos /> -->
    <DownloadSection />
    <FooterSection />
    
  </div>
</template>

<script setup lang="ts">

import Carousel from '../components/layout/Carousel.vue'
// import HeroSection from '../components/HeroSection.vue'
import LatestVideos from '../components/video/LatestVideos.vue'
import FeatureSection from '../components/home/FeatureSection.vue'
import DownloadSection from '../components/home/DownloadSection.vue'
import FooterSection from '../components/layout/FooterSection.vue'

import SpiritualWall from '../components/layout/SpiritualWall.vue'
import EventStatsCarousel from '../components/layout/EventStatsCarousel.vue'
import HomeVideoPreview from '../components/video/HomeVideoPreview.vue'

</script>

<style scoped>
</style>
