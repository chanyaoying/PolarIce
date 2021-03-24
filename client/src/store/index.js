import Vue from 'vue';
import Vuex from 'vuex';
import sampleQuestions from "./sampleQuestions"

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        nickname: "",
        roomID: '',
        currentComponent: 'gameLobby',
        currentQuestion: 0, // changes as the prof clicks next
        loadedQuestions: [], // the questions in the game
        users: [],
        chatHistory: {},
        selfQuestion: [],
        questions: sampleQuestions,
    },
    mutations: {
        setNickname(state, nickname) {
            state.nickname = nickname
        },
        setRoomID(state, roomID) {
            state.roomID = roomID
        },
        updateChat(state, {
            roomID,
            message
        }) {
            let repeat = true;
            if (typeof state.chatHistory[roomID] == "undefined") {
                Vue.set(state.chatHistory, roomID, [message]);
            } else {
                state.chatHistory[roomID].push(message) ? repeat : 0
            }
        },
        updateChatNoRepeat(state, {
            roomID,
            message
        }) {
            if (typeof state.chatHistory[roomID] == "undefined") {
                Vue.set(state.chatHistory, roomID, [message]);
            } else {
                if (state.chatHistory[roomID][state.chatHistory[roomID].length - 1] != message) {
                    state.chatHistory[roomID].push(message)
                }
            }
        },
        receivePlayers(state, payload) {
            state.users = payload
        },
        changeComponent(state, payload) {
            state.currentComponent = payload
        },
        nextQuestion(state, data) {
            state.currentQuestion = data
        },
        getQuestions(state, data) {
            state.loadedQuestions = data
        },
    },
    actions: {
        socket_updateChat({
            commit
        }, data) {
            commit("updateChat", data)
        },
        socket_updateChatNoRepeat({
            commit
        }, data) {
            commit("updateChatNoRepeat", data)
        },
        socket_setNickname({
            commit
        }, data) {
            commit("setNickname", data)
        },
        socket_receivePlayers({
            commit
        }, data) {
            commit("receivePlayers", data)
        },
        socket_changeComponent({
            commit
        }, data) {
            commit("changeComponent", data)
        },
        socket_nextQuestion({commit}, data) {
            commit("nextQuestion", data)
        },
        socket_getQuestions({commit}, data) {
            commit("getQuestions", data)
        }
    },
    modules: {}
})

// export const store = new Vuex.Store({});