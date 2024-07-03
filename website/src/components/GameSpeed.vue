<template>
    <div class="container py-4">
      <div class="p-5 mb-4 bg-body-tertiary rounded-3">
        <br>
          <center>
          <div class="card">
            <div class="card-body">
                <div class="container-fluid py-5">
                  <h1 class="display-5 fw-bold">Test your typing skills!</h1>
                  <p class="col-md-8 fs-4">Typing speed  !</p>

                  <div v-if="!isFinished">
                  <div class="row g-0 text-center p-2 mb-4" style="background-color: #ced4da">
                    <div class="col-sm-6 col-md-12 display-6 p-3">
                      <span class="m-lg-2" v-for="(word,key) in filteredWords" :key="key" v-bind:class="key!==0 || checkWrittenWord">
                        {{word  + ' '}}
                      </span></div>
                  </div>
                  <div class="input-group">
                  <input class="form-control form-control-lg" type="text" placeholder="Start typing the words above..." v-model="writtenWord">
                    <br>
                      <span class="input-group-text">{{timer}} seconds</span>
                    <br>
                    <br>
                      <button :disabled="this.isStarted" type="button" class="input-group-lg btn btn-primary" @click="setWords">Reload</button>
                    <br>
                  </div>
                  </div>
                  <div v-else><br>
                    <h2>Results</h2>
                      <div style="font-size: x-large"><b>True Count:</b> {{trueCount}}<br>
                      <b>False Count:</b> {{falseCount}}<br>
                      <b>Total Words:</b> {{trueCount + falseCount}}<br>
                      <b>Accuracy:</b> {{accuracyPercentage}}%</div><br>
                    <button type="button" @click="newGame" class="btn btn-primary btn-lg mt-1">Start A New Test!</button>
                  </div>
                </div>
            </div>
          </div>
          </center>
        <br>
        <button @click="shapeGame">Commencer le second jeu</button>
      </div>

      <footer class="pt-3 mt-4 text-body-secondary border-top">
        &copy; 2023
      </footer>
    </div>
</template>

<script>

import wordList from '../assets/commonWords.json'

export default {
  data () {
    return {
      words: [],
      writtenWord: null,
      trueCount: 0,
      falseCount: 0,
      isCorrect: true,
      timer: 60,
      interval: false,
      isStarted: false,
      isFinished: false,
      wordList: wordList
    }
  },
  watch: {
    writtenWord (value) {
      if (!value || value === ' ') {
        this.writtenWord = ''
        return
      }
      if (!this.isStarted) this.toggleTimer()
      const trueWord = this.words[0].slice(0, value.length)
      this.isCorrect = trueWord === value.replace(' ', '')

      if (value.indexOf(' ') !== -1) {
        this.isCorrect ? this.trueCount++ : this.falseCount++
        this.words.splice(0, 1)
        this.writtenWord = ''
        this.isCorrect = true
      }
    }
  },
  computed: {
    checkWrittenWord () {
      return this.isCorrect ? 'selected-word fw-semibold' : 'selected-word fw-semibold bg-danger'
    },
    filteredWords () {
      return this.words.filter((data, index) => index < 7)
    },
    accuracyPercentage () {
      return (100 / (this.trueCount + this.falseCount) * this.trueCount).toFixed(1)
    }
  },
  mounted () {
    this.setWords()
  },
  methods: {
    shapeGame() {
      this.$router.push('/game-shape');
    },
    newGame () {
      this.setWords()
      this.timer = 60
      this.isCorrect = true
      this.isFinished = false
      this.isStarted = false
      this.trueCount = 0
      this.falseCount = 0
      this.writtenWord = ''
    },
    toggleTimer () {
      this.isStarted = true
      this.interval = setInterval(() => {
        if (this.timer === 0 || this.timer < 1) {
          clearInterval(this.interval)
          this.isFinished = true
          return
        }
        this.timer--
      }, 1000)
    },
    setWords () {
      this.words = this.wordList.sort(() => Math.random() - 0.5)
    }
  }

}
</script>

<style>
.selected-word{
  padding: 5px;
  border-radius: 5px;
  background-color: rgb(222,184,135);
}
</style>