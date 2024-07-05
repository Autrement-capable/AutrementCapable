<template>
  <div id="app">
    <div class="course-container">
      <CourseCard v-for="course in courses" :key="course.id" :course="course" />
    </div>
  </div>
</template>

<script>
import CourseCard from "./CourseCard.vue";

export default {
  name: "App",
  components: {
    CourseCard,
  },
  data() {
    return {
      courses: [],
    };
  },
  created() {
    this.fetchCourses();
  },
  methods: {
    async fetchCourses() {
      try {
        const response = await fetch("http://localhost:5000/courses");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        this.courses = await response.json();
      } catch (error) {
        console.error("Error fetching courses:", error);
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.course-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
  padding-bottom: 100px;
}
</style>
