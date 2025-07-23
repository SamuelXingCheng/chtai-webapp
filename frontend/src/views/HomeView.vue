<template>
  <div>
    <NavBar />
    <Carousel />
    <div class="bg-beige w-full">
      <div class="max-w-7xl mx-auto px-4 py-10 grid md:grid-cols-2 gap-3 pt-3 pb-3">
        <EventStatsCarousel />
        <SpiritualWall />
      </div>
    </div>
    <!-- <HeroSection /> -->
    <FeatureSection />
    <LatestVideos />
    <DownloadSection />
    <FooterSection />
    
  </div>
</template>

<script setup lang="ts">
import NavBar from '../components/NavBar.vue'
import Carousel from '../components/Carousel.vue'
// import HeroSection from '../components/HeroSection.vue'
import LatestVideos from '../components/LatestVideos.vue'
import FeatureSection from '../components/FeatureSection.vue'
import DownloadSection from '../components/DownloadSection.vue'
import FooterSection from '../components/FooterSection.vue'

import SpiritualWall from '../components/SpiritualWall.vue'
import EventStatsCarousel from '../components/EventStatsCarousel.vue'

</script>

<style scoped>
</style>
