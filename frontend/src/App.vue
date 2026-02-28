<script setup>
import { ref, onMounted } from 'vue'

const apiMessage = ref(null)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await fetch('/api/hello')
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    apiMessage.value = data.message
  } catch (e) {
    error.value = 'Impossible de joindre le backend'
    console.error(e)
  }
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-blue-950 to-slate-900 flex items-center justify-center">
    <div class="text-center space-y-8 p-12">
      <!-- Titre principal -->
      <h1 class="text-6xl font-bold text-white tracking-tight">
        Demat Bed
        <img src="./img/flag_breton.png" alt="Gwenn-ha-du" class="inline-block h-12 ml-2 align-baseline rounded-lg" />
      </h1>

      <p class="text-xl text-blue-200/80 max-w-md mx-auto">
        Plateforme de validation collaborative du corpus parallèle breton–français
      </p>

      <!-- Réponse API -->
      <div
        v-if="apiMessage"
        class="inline-flex items-center gap-2 rounded-full bg-emerald-500/15 border border-emerald-400/30 px-6 py-2 text-emerald-300 text-sm backdrop-blur"
      >
        <span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
        API connectée — {{ apiMessage }}
      </div>

      <div
        v-else-if="error"
        class="inline-flex items-center gap-2 rounded-full bg-red-500/15 border border-red-400/30 px-6 py-2 text-red-300 text-sm backdrop-blur"
      >
        <span class="h-2 w-2 rounded-full bg-red-400" />
        {{ error }}
      </div>

      <div v-else class="text-blue-300/50 text-sm animate-pulse">
        Connexion à l'API…
      </div>
    </div>
  </div>
</template>
