import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueSocketIOExt  from 'vue-socket.io-extended';
import io from 'socket.io-client'; 

const socket = io('http://' + document.domain + ':' + "5001")
Vue.use(VueSocketIOExt, socket, store);

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App),

}).$mount('#app')
