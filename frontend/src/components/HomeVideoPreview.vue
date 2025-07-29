<template>
  <section class="bg-white rounded-xl shadow p-4 space-y-8">
    <!-- 本週信息影音精選 -->
    <section class="space-y-4">
      <h2 class="text-lg font-semibold text-gray-800 flex items-center gap-2">
        <svg class="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4l12 6-12 6V4z" /></svg>
        一年七次特會訓練 精選
      </h2>
      <VideoGrid :videos="infoVideos" @play="openVideo" />
    </section>

    <!-- 兒童影音精選 -->
    <section class="space-y-4">
      <h2 class="text-lg font-semibold text-gray-800 flex items-center gap-2">
        <svg class="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4l12 6-12 6V4z" /></svg>
        兒童影音 精選
      </h2>
      <VideoGrid :videos="childrenVideos" @play="openVideo" />
    </section>

    <!-- 福音詩歌精選 - 嵌入 SoundCloud -->
    <section class="space-y-4">
      <h2 class="text-lg font-semibold text-gray-800 flex items-center gap-2">
        <svg class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4l12 6-12 6V4z" /></svg>
        福音詩歌 精選
      </h2>
        <!-- ✅ 嵌入播放器 -->
        <div class="rounded-xl overflow-hidden shadow">
            <iframe
            id="sc-player"
            width="100%"
            height="300"
            scrolling="no"
            frameborder="no"
            allow="autoplay"
            :src="soundcloudEmbedUrl"
            class="rounded-xl"
            ></iframe>
        </div>
    </section>

    <FloatingPlayer ref="floatingPlayerRef" />
  </section>
</template>


<script setup>
import { ref } from 'vue'
import FloatingPlayer from '../components/FloatingPlayer.vue' // 確保路徑正確
import VideoGrid from '../components/VideoGrid.vue'

const floatingPlayerRef = ref()

const previewVideos = ref([
  {
    id: 'abc123',
    title: '台中清晨禱研背講',
    source: '台中市召會',
    videoUrl: 'https://www.youtube.com/watch?v=9HuKURB5fSo',
    coverImage: 'https://img.youtube.com/vi/9HuKURB5fSo/0.jpg',
  },
  {
    id: 'def456',
    title: '李俊輝弟兄 要點交通',
    source: '晨興聖言 / 要點複習 / 李俊輝',
    videoUrl: 'https://www.youtube.com/watch?v=FvdjKZfe8gw&list=PLgy5Els6ka2LlPyNbAahFKuxjWiOfhVoF&index=7',
    coverImage: 'https://img.youtube.com/vi/vdjKZfe8gw&list=PLgy5Els6ka2LlPyNbAahFKuxjWiOfhVoF&index=7/0.jpg',
  },
])

const infoVideos = ref([
  { id: 'v1', title: '台中清晨禱研背講', source: '台中市召會', 
  videoUrl: 'https://www.youtube.com/watch?v=9HuKURB5fSo', 
  coverImage: 'https://img.youtube.com/vi/9HuKURB5fSo/0.jpg' },

  { id: 'v2', title: '李俊輝弟兄 要點交通', source: '台中市召會', 
  videoUrl: 'https://youtu.be/FvdjKZfe8gw/watch?v=FvdjKZfe8gw', 
  coverImage: 'https://img.youtube.com/vi/FvdjKZfe8gw/0.jpg' }
  // 更多本週信息影音
])

const childrenVideos = ref([
  { id: 'v2', title: '兒童詩歌1', source: '兒童服事', videoUrl: '...', coverImage: '...' },
  // 更多兒童影音
])

const gospelVideos = ref([
  { id: 'v3', title: '福音短片1', source: '福音行動', videoUrl: '...', coverImage: '...' },
  // 更多福音影音
])

const soundcloudEmbedUrl =
  'https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/1871928719&color=%23D9D9D9&auto_play=false&hide_related=true&show_comments=false&show_user=false&show_reposts=false&show_teaser=false&visual=false'


const openVideo = (url) => {
  floatingPlayerRef.value?.open(url)
}
</script>