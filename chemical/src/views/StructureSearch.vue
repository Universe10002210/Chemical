<template>
  <div class="structural - search">
    <header>
      <h1>Chemical Book</h1>
      <input type="text" placeholder="请输入产品名称、CAS号查询" v - model="searchText">
      <button @click="performSearch">搜索</button>
      <button @click="openStructuralSearch">结构式搜索</button>
    </header>
    <main>
      <div class="drawing - area">
        <div id="jsmol - container"></div>
      </div>
      <div class="cas - conversion">
        <input type="text" placeholder="请输入CAS No." v - model="casNumber">
        <button @click="convertCAS">转换为结构式</button>
      </div>
      <div class="image - conversion">
        <input type="file" id="image - input" @change="handleImageUpload">
        <label for="image - input">选择图片</label>
        <p>[Ctrl+V可粘贴图片]</p>
        <button @click="convertImageToStructure">转换图片为结构式</button>
      </div>
      <div class="search - conditions">
        <input type="radio" id="sub - structure" name="search - type" value="sub - structure" v - model="searchType" checked>
        <label for="sub - structure">子结构搜索</label><br>
        <input type="radio" id="exact" name="search - type" value="exact" v - model="searchType">
        <label for="exact">精确搜索</label><br>
        <input type="radio" id="90 - similar" name="search - type" value="90 - similar" v - model="searchType">
        <label for="90 - similar">90%相似搜索</label><br>
        <input type="radio" id="60 - similar" name="search - type" value="60 - similar" v - model="searchType">
        <label for="60 - similar">60%相似搜索</label><br>
        <input type="radio" id="30 - similar" name="search - type" value="30 - similar" v - model="searchType">
        <label for="30 - similar">30%相似搜索</label><br>
        <button @click="performSearchWithConditions">Search</button>
      </div>
    </main>
  </div>
</template>

<script>
import JSMol from 'jsmol';
import axios from 'axios';

export default {
  data() {
    return {
      searchText: '',
      casNumber: '',
      searchType: 'sub - structure',
      jmol: null
    };
  },
  mounted() {
    this.initJSMol();
  },
  methods: {
    initJSMol() {
      const jsmolDiv = document.getElementById('jsmol - container');
      this.jmol = JSMol.getApplet(jsmolDiv);
      this.jmol.script('load c1ccccc1');
    },
    performSearch() {
      // 这里添加普通搜索逻辑，调用后端API等
      console.log('执行普通搜索', this.searchText);
    },
    openStructuralSearch() {
      // 这里可以添加打开结构式搜索相关逻辑，比如切换页面等
      console.log('打开结构式搜索');
    },
    convertCAS() {
      axios.get(`https://api.example.com/cas - to - structure?cas=${this.casNumber}`)
       .then(response => {
          // 处理返回的结构式数据，例如在jsmol中显示
          const structureData = response.data;
          this.jmol.script(`load ${structureData}`);
        })
       .catch(error => {
          console.error('转换错误', error);
        });
    },
    handleImageUpload() {
      const file = document.getElementById('image - input').files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const imageData = e.target.result;
          this.convertImage(imageData);
        };
        reader.readAsDataURL(file);
      }
    },
    convertImageToStructure() {
      // 这里添加粘贴图片转换逻辑，获取粘贴板图片数据等
      console.log('转换粘贴图片为结构式');
    },
    convertImage(imageData) {
      // 调用图片识别函数，将图片转换为结构式数据，这里只是示例，需实际对接识别服务
      console.log('处理图片数据', imageData);
    },
    performSearchWithConditions() {
      // 根据searchType调用后端API进行搜索
      console.log('根据条件执行搜索', this.searchType);
    }
  }
};
</script>

<style scoped>
.structural-search {
  font-family: Arial,sans-serif;
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  background-color: #f4f4f4;
}
main {
  display: flex;
  padding: 10px;
}
.drawing-area {
  width: 50%;
  border: 1px solid #ccc;
}
.cas-conversion,
.image-conversion,
.search-conditions {
  width: 50%;
  padding: 10px;
  border: 1px solid #ccc;
  margin-left: 10px;
}
button {
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}
input[type="radio"] {
  margin-right: 5px;
}
</style>
