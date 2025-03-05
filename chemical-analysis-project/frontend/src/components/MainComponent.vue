
<template>
    <div>
        <input type="file" @change="handleFileUpload" accept=".sdf,.mol,.chemic">
        <div v-if="results">
            <h3>搜索结果：</h3>
            <div v-for="item in results" :key="item.name">
                <div :style="{ color: getColor(item.similarity) }">
                    {{ item.name }} - 相似度: {{ item.similarity }}
                </div>
                <mol-view :smiles="item.smiles" />
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import MolView from './MolView.vue';

export default {
    components: { MolView },
    data() {
        return { results: null };
    },
    methods: {
        async handleFileUpload(event) {
            const file = event.target.files[0];
            const formData = new FormData();
            formData.append('file', file);

            // 上传并解析分子
            const uploadRes = await axios.post('http://localhost:5000/upload', formData);
            const inchi = uploadRes.data.inchi;

            // 查询相似化合物
            const searchRes = await axios.post('http://localhost:5000/search', {
                smiles: Chem.MolToSmiles(Chem.MolFromInchi(inchi)),
                threshold: 0.8,
                method: 'tanimoto' // 可扩展支持更多方法
            });
            this.results = searchRes.data.results;
        },
        getColor(similarity) {
            if (similarity >= 0.98) return 'black';
            if (similarity >= 0.8) return 'red';
            return 'yellow';
        }
    }
};
</script>
