import Vue from 'vue';
import Vuex from 'vuex';
import sampleQuestions from "./sampleQuestions"


Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        userData: {},
        finalQuestion: [],
        nickname: "",
        roomID: '', // this room ID is the ID of the room that the user is currently in. e.g. Test Room
        currentComponent: 'gameLobby',
        currentQuestion: 0, // changes as the prof clicks next
        cachedQuestions: [], // the questions in the game
        users: [],
        chatHistory: {},
        questions: sampleQuestions,
        playerChoices: {},
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
            state.cachedQuestions = data
        },
        addPlayerChoices(state, {currentQuestion, choice}) {
            Vue.set(state.playerChoices, currentQuestion, choice)
        },
        addFinalQuestion(state, question_list) {
            var userCreated = []
            var firebase = []
            var testBank = []
            for (var question in question_list)
                if (question_list[question].dbsrc === 'user') {
                    userCreated.push(question_list[question])

                } else if (question_list[question].dbsrc === 'firebase') {
                firebase.push(question_list[question])

            } else {
                testBank.push(question_list[question])
            }

            state.finalQuestion.push({
                usercreated: userCreated,
                firebase: firebase,
                testBank: testBank
            });

        },
        setUserData(state, payload) {
            state.userData = payload
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
        },
        socket_changeComponent({
            commit
        }, data) {
            commit("changeComponent", data)
        },
        socket_nextQuestion({
            commit
        }, data) {
            commit("nextQuestion", data)
        },
        socket_getQuestions({
            commit
        }, data) {
            commit("getQuestions", data)
        },
        async_setUserData({
            commit
        }, data) {
            commit("setUserData", data)
        }

    },
    getters: {
        // GetCurrentQuestion(state) {
        //     return state.currentQuestion;
        // },
        GetFireBase(state) {
            return state.questions;
        },
        getLoadedQLength(state) {
            return state.cachedQuestions.length;
        }
    },
    modules: {}
})

// export const store = new Vuex.Store({});