<template>
<div id="base-list">
  <div class="about">
    <h1>検索</h1>
  </div>
  <form @submit.prevent="registration">
    <p class="error" v-if="error">{{ error }}</p>
    <p><input type="text" v-model="url" placeholder="url" name="url"/></p>
    <p>{{ url }}</p>
    <div class="signup-btn">
      <button type="submit">submit</button>
    </div>
  </form>
  <ul>
    <li v-for="item in baseList">
      {{item.region}}：{{item.visits}}
    </li>
  </ul>
</div>
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