<template>
  <section class="bg-beige pt-5 pb-3">
    <div class="max-w-7xl mx-auto px-4">
      <swiper
        :modules="modules"
        :slides-per-view="1"
        :loop="true"
        :autoplay="{ delay: 6000, disableOnInteraction: false }"
        :pagination="{ clickable: true }"
        :navigation="true"
        class="rounded-xl shadow"
        >
        <swiper-slide v-for="(slide, index) in slides" :key="index">
          <div class="bg-white p-6 md:p-10 flex flex-col-reverse lg:flex-row items-center gap-10 rounded-xl">
            <!-- 左側文字 -->
            <div class="flex-0.3">
              <p class="text-sm text-gray-500 mb-2">{{ slide.date }}</p>
              <h2 class="text-3xl md:text-4xl font-bold text-gray-800 leading-snug" v-html="slide.title"></h2>
              <p class="mt-4 text-gray-600">{{ slide.description }}</p>
              <button class="mt-6 text-white px-6 py-2 rounded bg-teal-500 hover:bg-teal-600 transition">
                了解更多
              </button>
            </div>

            <!-- 右側圖片 -->
            <div class="flex-1">
              <img :src="slide.image" :alt="slide.title" class="w-full h-60 object-cover rounded shadow" />
            </div>
          </div>
        </swiper-slide>
      </swiper>
    </div>
  </section>
</template>


<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Autoplay, Pagination, Navigation } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'
import 'swiper/css/navigation'

const base = import.meta.env.BASE_URL

const modules = [Autoplay, Pagination, Navigation]

const slides = [
  {
    date: '7/21 即將進入',
    title: '以弗所書<br/>生命讀經',
    description: '盼望你我都準備好，不要錯過相約一同天天共同追求！',
    image: `${base}banner-book.png`,
  },
  {
    date: '8/15 將舉行',
    title: '兒童服事訓練',
    description: '歡迎所有負責的弟兄姊妹參加，恢復主託付的照顧與教導',
    image: `${base}children-image.png`,
  },
]
</script>

<style scoped>
.swiper {
  width: 100%;
}
</style>
