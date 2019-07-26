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
      tags: [],
      jsonList:[],
      dayList:[],
      weekList:[],
      mounthList:[]
    }
  },
  // asyncDataでレンダリング前にAPIを呼ぶ
  asyncData () {
    jsonList: process.env.jsonList
  },
  mounted () {
    const kyotenId = this.$nuxt.$route.query.kyoten;
    
    const jsonList = process.env.jsonList;
    const dayAry = jsonList.filter(function(url){
      const pattern = new RegExp('static/data/inter/day/' + '([0-9]*)' + kyotenId + '.json', 'gi');
      return url.match(pattern);
    });
    const weekAry = jsonList.filter(function(url){
      const pattern = new RegExp('static/data/inter/week/' + '([0-9]*)' + kyotenId + '.json', 'gi');
      return url.match(pattern);
    });
    const monthAry = jsonList.filter(function(url){
      const pattern = new RegExp('static/data/inter/month/' + '([0-9]*)' + kyotenId + '.json', 'gi');
      return url.match(pattern);
    });

    for(const n in dayAry){
      const jsonPath = dayAry[n];
      const temp = jsonPath.match(/([0-9]{4})([0-9]{2})([0-9]{2})/);
      this.dayList[n] = {id:temp[0],name:temp[1]+'年'+temp[2]+'月'+temp[3]+'日'};
    }
    
    for(const n in weekAry){
      const jsonPath = weekAry[n];
      const temp = jsonPath.match(/([0-9]{4})([0-9]{2})([0-9]{2})/);
      this.weekList[n] = {id:temp[0],name:temp[1]+'年'+temp[2]+'月'+temp[3]+'日'};
    }

    for(const n in monthAry){
      const jsonPath = monthAry[n];
      const temp = jsonPath.match(/([0-9]{4})([0-9]{2})([0-9]{2})/);
      this.monthList[n] = {id:temp[0],name:temp[1]+'年'+temp[2]+'月'+temp[3]+'日'};
    }
    console.log(this.dayList);
    console.log(this.weekList);
    console.log(this.monthList);
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
        tmp_tags = this.dayList;
      } else if (this.selectedCategory == 'week') {
        tmp_tags = this.weekList;
      } else if (this.selectedCategory == 'mounth') {
        tmp_tags = this.monthList; 
      } else {
        alert('Invalid value!!')
      }
      
      this.tags = tmp_tags;
      this.senmon();
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