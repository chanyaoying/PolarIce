import Vue from 'vue';
import Vuex from 'vuex';
import sampleQuestions from "./sampleQuestions"

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        nickname: "",
        roomID: '',
        currentComponent: 'gameLobby',
        currentQuestion: '', // changes as the prof clicks next
        loadedQuestions: {}, // the game
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
        updateChatNoRepeat(state, {roomID, message}) {
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
        }
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
        }
    },
    modules: {}
})

// export const store = new Vuex.Store({});