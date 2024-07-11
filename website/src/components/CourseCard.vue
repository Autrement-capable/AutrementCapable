<template>
  <div class="course-card">
    <img :src="course.image" alt="Course Image" class="course-image" />
    <h3>{{ course.name }}</h3>
    <a :href="course.url" target="_blank">Go to Course</a>
  </div>
</template>

<script>
export default {
  name: "CourseCard",
  props: {
    course: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.course-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  max-width: 300px;
  min-width: 200px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}

.course-image {
  width: 200px;
  height: 200px;
  object-fit: fill;
  border-radius: 8px;
}

.course-card h3 {
  margin: 16px 0;
}
</style>
