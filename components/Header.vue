<template>
  <nav class="navbar is-white" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <div class="navbar-item">アクセスレポート</div>
      <div class="navbar-burger" data-target="navMenu">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div><!-- navbar-brand END -->
    <div class="navbar-menu" id="navMenu">
      <div class="navbar-end">
        <nuxt-link to="/" class="navbar-item">トップ</nuxt-link>
      </div>
    </div><!-- navbar-menu END -->
  </nav>
</template>
<script>

export default {
  data: () => ({
    showNav: false,
    items: [
      { title: 'Home', icon: 'home', url: '/' },
      { title: 'Feature', icon: 'code', url: '/feature' },
      { title: 'Contact', icon: 'question_answer', url: '/contact' }
    ]
  })
}
</script>

<style>
.navbar {
  margin-bottom: 20px;
}
.burger-font-icon img {
  height: 30px;
  margin: 10px 0 0 12px;
}
</style>