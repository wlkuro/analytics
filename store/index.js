export const state = () => ({
  authUser: null,
})

export const mutations = {
  SET_USER: function (state, data) {
    if (data) {
      state.authUser = data
    } else {
      state.authUser = null 
    }
  }
}

export const actions = {
  async login({ commit }, { username, password }) {
    try {
      //const res = await axios.post('/login', { username, password })  本当は、たぶんこんな感じ
      if (username != "demo" || password != "pass") {
        throw new Error("エラーですよ")
      }
      commit('SET_USER', username)
    } catch (error) {
      throw error
    }
  },
  async logout({ commit }) {
    try {
      commit('SET_USER', null)
    } catch(error) {
      throw error
    }
  }
}