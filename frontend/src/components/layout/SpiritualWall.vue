<!-- src/components/layout/SpiritualWall.vue -->
<script setup lang="ts">
import { ref } from 'vue'

const posts = ref([
  { id: 1, content: '今天聚會真實享受主的同在！', time: '3 分前', amens: 1 },
  { id: 2, content: '因祂的恩典，我們得以經歷新的一天', time: '1 小時前', amens: 9 },
  { id: 3, content: '主，祢是我隨時的幫助！', time: '2 小時前', amens: 12 },
  { id: 4, content: '祂是信實的，永不撇下我', time: '1 天前', amens: 23 },
])

const newPost = ref('')
const isAnonymous = ref(true)

const submitPost = () => {
  if (newPost.value.trim() === '') return
  posts.value.unshift({
    id: Date.now(),
    content: newPost.value,
    time: '剛剛',
    amens: 0
  })
  newPost.value = ''
}
</script>

<template>
    <section class="bg-beige pt-1 pb-1">
        <div class="bg-white shadow-md rounded-lg p-5 w-full max-w-xl mx-auto ">
            <!-- 區塊標題 -->
            <h2 class="text-3xl font-bold text-gray-800 flex items-center mb-4">
            屬靈互動牆
            </h2>

            <!-- 貼文區 -->
            <ul class="space-y-3 mb-4">
            <li v-for="post in posts" :key="post.id" class="border-b pb-2">
                <div class="text-sm text-gray-500">匿名</div>
                <div class="text-gray-800">{{ post.content }}</div>
                <div class="text-xs text-gray-400 flex items-center gap-3 mt-1">
                <span>{{ post.time }}</span>
                <span class="flex items-center gap-1">🤍 {{ post.amens }} Amen</span>
                </div>
            </li>
            </ul>

            <!-- 發文區 -->
            <div class="mt-4">
            <textarea
                v-model="newPost"
                rows="2"
                placeholder="寫下一點屬靈感動…"
                class="w-full border rounded-md p-2 text-sm focus:outline-none focus:ring focus:border-blue-400 resize-none"
            />
            <div class="flex items-center justify-between mt-2">
                <label class="flex items-center text-sm text-gray-600">
                <input type="checkbox" v-model="isAnonymous" class="mr-1" />
                匿名
                </label>
                <button
                @click="submitPost"
                class="text-white px-4 py-1 rounded-md bg-teal-500	hover:bg-teal-600 text-sm"
                >
                發布
                </button>
            </div>
            </div>
        </div>
    </section>
</template>
