<template>
  <section class="container">
    <div id="base-list">
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="h3 mb-0 text-gray-800">専門店アクセスレポート</h1>
    </div>
    
    <div class="card shadow mb-4">
            <div class="card-header py-3">
              <h6 class="m-0 font-weight-bold text-primary">DataTables Example</h6>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <div id="dataTable_wrapper" class="dataTables_wrapper dt-bootstrap4"><div class="row"><div class="col-sm-12 col-md-6"><div class="dataTables_length" id="dataTable_length"><label>Show <select name="dataTable_length" aria-controls="dataTable" class="custom-select custom-select-sm form-control form-control-sm"><option value="10">10</option><option value="25">25</option><option value="50">50</option><option value="100">100</option></select> entries</label></div></div><div class="col-sm-12 col-md-6"><div id="dataTable_filter" class="dataTables_filter"><label>Search:<input type="search" class="form-control form-control-sm" placeholder="" aria-controls="dataTable"></label></div></div></div><div class="row"><div class="col-sm-12"><table class="table table-bordered dataTable" id="dataTable" width="100%" cellspacing="0" role="grid" aria-describedby="dataTable_info" style="width: 100%;">
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
                      <td class="sorting_1">{{item.title}}</td>
                      <td>{{item.visits}}</td>
                    </tr>
                  </tbody>
                </table></div></div><div class="row"><div class="col-sm-12 col-md-5"><div class="dataTables_info" id="dataTable_info" role="status" aria-live="polite">Showing 1 to 57 of 57 entries</div></div><div class="col-sm-12 col-md-7"><div class="dataTables_paginate paging_simple_numbers" id="dataTable_paginate"><ul class="pagination"><li class="paginate_button page-item previous disabled" id="dataTable_previous"><a href="#" aria-controls="dataTable" data-dt-idx="0" tabindex="0" class="page-link">Previous</a></li><li class="paginate_button page-item active"><a href="#" aria-controls="dataTable" data-dt-idx="1" tabindex="0" class="page-link">1</a></li><li class="paginate_button page-item next disabled" id="dataTable_next"><a href="#" aria-controls="dataTable" data-dt-idx="2" tabindex="0" class="page-link">Next</a></li></ul></div></div></div></div>
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
      password: ""
    }
  },
  // asyncDataでレンダリング前にAPIを呼ぶ
  /*asyncData() {
    const urls = import(`~/static/senmon.json`);
    console.log(urls);
    return {urls}
  },*/
  mounted () {
    this.senmon();
  },
  methods: {
    async senmon() {
      const results = [];
      var tempArr = [];
      var obj = {};
      var count = 0;
      const urls = await import(`~/static/senmon.json`);
      for (const num in urls['inter']) {
        console.log(urls['inter'][num]);
        obj = await axios.get('http://34.85.119.45:8080/api/senmon', {
          params: {
            // ここにクエリパラメータを指定する
            url: urls['inter'][num].path,
            deptName: '関東発'
          }
        }).then(res => {
          // asyncDataでreturnしたものはdataにマージされる
          if(res.data[0] != null){
            this.baseList[count] = res.data[0];
            this.baseList.splice();
            count++;
          }
          return res.data
        })
        /*this.baseList[count] = obj[0];
        count++;*/
      }
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