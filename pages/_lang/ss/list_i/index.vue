<template>
  <section class="container">
    <div id="base-list">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="h3 mb-0 text-gray-800">専門店アクセスレポート</h1>
    </div>
    
    <div class="card shadow mb-4">
            <div class="card-body">
              <div class="table-responsive">
                <div id="dataTable_wrapper" class="dataTables_wrapper dt-bootstrap4">
                  <div class="row">
                    <div class="col-sm-12 col-md-6">
                      <div class="dataTables_length" id="dataTable_length">
                        <label>
                          <select name="category" v-model="selectedCategory" v-on:change="fetchTags" aria-controls="dataTable" class="custom-select custom-select-sm form-control form-control-sm">
                            <option v-for="category in categories" v-bind:value="category.id">
                              {{ category.name }}
                            </option>
                        </select> </label>
                        </div>
                      </div>
                      <div class="col-sm-12 col-md-6">
                        <div class="dataTables_length" id="dataTable_length">
                          <label>
                          
                          <select name="tag" v-model="selectedTag" v-on:change="senmon" class="custom-select custom-select-sm form-control form-control-sm">
                            <option v-for="tag in tags" v-bind:value="tag.id">
                              {{ tag.name }}
                            </option>
                          </select>
                          </label>
                        </div>
                      </div>
                    </div>
            <div class="row">
              <div class="col-sm-12">
                <table class="table table-bordered dataTable" id="dataTable" width="100%" cellspacing="0" role="grid" aria-describedby="dataTable_info" style="width: 100%;">
                  <thead>
                    <tr role="row">
                      <th class="sorting_asc" tabindex="0" aria-controls="dataTable" rowspan="1" colspan="1" aria-sort="ascending" aria-label="Name: activate to sort column descending" style="width: 186px;">ページタイトル</th>
                      <th class="sorting" tabindex="0" aria-controls="dataTable" rowspan="1" colspan="1" aria-label="Position: activate to sort column ascending" style="width: 282px;">表示回数</th>
                    </tr>
                  </thead>
                  <tfoot>
                    <tr>
                      <th rowspan="1" colspan="1">ページタイトル</th>
                      <th rowspan="1" colspan="1">表示回数</th>
                    </tr>
                  </tfoot>
                  <tbody>
                    <tr v-for="item in baseList">
                      <td class="sorting_1">{{item.title}}<br><a :href="item.pagePath" target="_blank" class="small">{{item.pagePath}}</a></td>
                      <td>{{item.pageviews_y}}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="row">
            </div><div class="col-sm-12 col-md-7">
            <div class="dataTables_paginate paging_simple_numbers" id="dataTable_paginate">
            </div>
            </div>
            </div>
            </div>
              </div>
            </div>
          </div>
    
    

    </div>
  </section>
</template>
<script>
import axios from 'axios'

export default {
  data: function() {
    return {
      baseList: [],
      error: null,
      urls: {},
      password: "",
      selectedCategory: 'day',
      selectedTag: '20190710',
      categories: [],
      tags: []
    }
  },
  // asyncDataでレンダリング前にAPIを呼ぶ
  syncData() {
    const path = require('path');
    const fs = require('fs');

    const target = '/home/mac/nuxt-express-template/static/data/inter/';
    const dirPath = path.resolve(__dirname, target);

    const list = fs.readdirSync(dirPath);
    list.forEach(console.log);
  },
  mounted () {
    this.categories[0] = {id: 'day', name: 'day'}
    this.categories[1] = {id: 'week', name: 'week'}
    this.categories[2] = {id: 'mounth', name: 'mounth'}
    this.categories.splice();
    this.senmon();
  },
  methods: {
    fetchTags: function() {
      var tmp_tags = [];
      
      if (this.selectedCategory == 'day') {
        tmp_tags = [
          {id: 20190710, name: '2019年7月4日'},
          {id: 20190703, name: '2019年7月3日'},
          {id: 20190702, name: '2019年7月2日'},
          {id: 20190701, name: '2019年7月1日'},
          {id: 20190630, name: '2019年6月30日'},
        ]
      } else if (this.selectedCategory == 'week') {
        tmp_tags = [
          {id: 20190630, name: '2019年6月30日'},
          {id: 20190623, name: '2019年6月23日'},
        ]
      } else if (this.selectedCategory == 'mounth') {
        tmp_tags = [
          {id: 20190701, name: '2019年7月1日'},
          {id: 20190601, name: '2019年6月1日'},
        ]      
      } else {
        alert('Invalid value!!')
      }
      
      this.tags = tmp_tags;
    },
    async senmon() {
      const results = [];
      var tempArr = [];
      var obj = {};
      var count = 0;
      
      console.log(this.selectedCategory);
      console.log(this.selectedTag);
      this.baseList = [];
      this.baseList.splice();
        const query = Object.assign({}, this.$route.query);
        const temp = await import(`~/static/data/inter/`+this.selectedCategory+`/`+this.selectedTag+query['kyoten']+`.json`);
        const jsonData = JSON.parse(temp[0]);
        console.log(jsonData);
        for(const num in jsonData){
          const oobj = jsonData[num];
        console.log(oobj);
          if(oobj.title != null){
            const tempTitle = oobj.title
            //北海道発 ブラジル旅行 ブラジルツアー｜海外旅行 海外ツアー｜阪急交通社
            var regex = /.*?\s.*?/g;
            const titleArr = tempTitle.match(regex)
            oobj.title = titleArr[1];
            oobj.pagePath = 'https://hankyu-travel.com'+oobj.pagePath;

            console.log(oobj.title);
            this.baseList[count++] = oobj;
          }
        }
        this.baseList.splice();
        console.log(this.baseList);
    },
    async login() {
      try {
        await this.$store.dispatch('login', {
            username: this.url
        })
        this.$router.push('/')
      } catch(e) {
        this.formError = e.message
      }
    },
  }
}
</script>