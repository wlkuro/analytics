<template>
  <section class="container">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="h3 mb-0 text-gray-800">拠点アクセスレポート</h1>
    </div>
    <div class="card-deck">
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">キーワード検索</h4>
          <a href="/search" class="btn btn-primary">Go somewhere</a>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">専門店アクセス数</h4>
          <a href="/ss" class="btn btn-primary">Go somewhere</a>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <h4 class="card-title">全国特集アクセス数</h4>
          <a href="/lp" class="btn btn-primary">Go somewhere</a>
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
      baseList: {},
      error: null,
      url: "",
      password: ""
    }
  },
  // asyncDataでレンダリング前にAPIを呼ぶ
  /*asyncData(context) {
    return axios.get('http://34.85.119.45:3000/api/base', {
      params: {
        // ここにクエリパラメータを指定する
        url: '/guide/kanto/'
      }
  }).then(res => {
      // asyncDataでreturnしたものはdataにマージされる
      return { baseList: res.data }
    })
  },*/
  methods: {
    async registration() {
      console.log(this.url);
      return axios.get('http://34.85.119.45:3000/api/base', {
        params: {
          // ここにクエリパラメータを指定する
          url: this.url
        }
      }).then(res => {
        console.log(res.data);
        const self = this
        // asyncDataでreturnしたものはdataにマージされる
        //this.$set(baseList, res.data)
        this.baseList = res.data;
        return { baseList: res.data }
      })
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