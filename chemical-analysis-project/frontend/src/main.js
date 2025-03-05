import { createApp } from 'vue'
// 假设 MainComponent.vue 是应用的根组件，若不是需替换为实际根组件
import MainComponent from './components/MainComponent.vue' 
const app = createApp(MainComponent)
app.mount('#app')