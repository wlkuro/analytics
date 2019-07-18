<template>
  <div id="wrapper">
    <div class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion">
      <my-sidemenu/>
    </div>
    <div id="content-wrapper" class="d-flex flex-column">
      <my-header/>
      <div id="content">
        <div class="container-fluid">
          <nuxt class="has-text-centered"/>
        </div>
      </div>
      <footer class="sticky-footer bg-white">
        <my-footer/>
      </footer>

    </div>
  </div>
</template>

<script>
import MyHeader from '~/components/Header.vue'
import MyFooter from '~/components/Footer.vue'
import MySidemenu from '~/components/Sidemenu.vue'

export default {
  components: {
    MyFooter,
    MyHeader,
    MySidemenu
  }
}
</script>

<style>
.site {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}
.siteContent {
  flex: 1;
}
</style>
