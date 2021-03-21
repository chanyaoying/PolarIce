import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    roomID:'',
    selfQuestion:[],
    questions:[{question:'Are you a cat or dog person?', choice:['Cat','Dog']},
                {question:'Are you a happy or sad person?', choice:['Happy','Sad']},
                {question:'Are you a female or male person?', choice:['Female','Male']},
                {question:'Are you a introvert or extrovert person?', choice:['Introvert','Extrovert']},
                {question:'Are you a tall or short person?', choice:['Tall','Short']},
                {question:'I think carefully before I say something.?', choice:['YES','NO']},
                {question:'I’m a “Type A” go-getter. I’d rather die than quit.', choice:['YES','NO']},
                {question:'I feel overwhelmed and I’m not sure what to change.', choice:['YES','NO']},
                {question:'I make decisions based on logic.', choice:['YES','NO']},
                {question:'I appreciate it when someone gives me their undivided attention.', choice:['YES','NO']}, 
              ]
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})

// export const store = new Vuex.Store({});


