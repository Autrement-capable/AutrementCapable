<template>
    <div>
      <h1>Random Avatar Generator</h1>
      <div id="avatar">
        <img :src="avatarUrl" alt="Avatar" id="avatar-image">
      </div>
      <div>
        <button @click="changeParameter('style', 'prev')">Previous Style</button>
        <button @click="changeParameter('style', 'next')">Next Style</button>
      </div>
      <div>
        <button @click="changeParameter('background_color', 'prev')">Previous Background Color</button>
        <button @click="changeParameter('background_color', 'next')">Next Background Color</button>
      </div>
      <div>
        <button @click="changeParameter('hairstyle', 'prev')">Previous Hairstyle</button>
        <button @click="changeParameter('hairstyle', 'next')">Next Hairstyle</button>
      </div>
      <div>
        <button @click="changeParameter('clothing_color', 'prev')">Previous Clothing Color</button>
        <button @click="changeParameter('clothing_color', 'next')">Next Clothing Color</button>
      </div>
      <div>
        <button @click="changeParameter('eyebrows', 'prev')">Previous Eyebrows</button>
        <button @click="changeParameter('eyebrows', 'next')">Next Eyebrows</button>
      </div>
      <div>
        <button @click="changeParameter('eyes', 'prev')">Previous Eyes</button>
        <button @click="changeParameter('eyes', 'next')">Next Eyes</button>
      </div>
      <div>
        <button @click="changeParameter('nose', 'prev')">Previous Nose</button>
        <button @click="changeParameter('nose', 'next')">Next Nose</button>
      </div>
      <div>
        <button @click="changeParameter('mouth', 'prev')">Previous Mouth</button>
        <button @click="changeParameter('mouth', 'next')">Next Mouth</button>
      </div>
      <div>
        <button @click="changeParameter('facial_hair', 'prev')">Previous Facial Hair</button>
        <button @click="changeParameter('facial_hair', 'next')">Next Facial Hair</button>
      </div>
      <div>
        <button @click="changeParameter('skin_color', 'prev')">Previous Skin Color</button>
        <button @click="changeParameter('skin_color', 'next')">Next Skin Color</button>
      </div>
      <div>
        <button @click="changeParameter('hair_color', 'prev')">Previous Hair Color</button>
        <button @click="changeParameter('hair_color', 'next')">Next Hair Color</button>
      </div>
      <div>
        <button @click="changeParameter('accessory', 'prev')">Previous Accessory</button>
        <button @click="changeParameter('accessory', 'next')">Next Accessory</button>
      </div>
      <div>
        <button @click="changeParameter('clothing', 'prev')">Previous Clothing</button>
        <button @click="changeParameter('clothing', 'next')">Next Clothing</button>
      </div>
      <div>
        <button @click="changeParameter('clothing_graphics', 'prev')">Previous Clothing Graphics</button>
        <button @click="changeParameter('clothing_graphics', 'next')">Next Clothing Graphics</button>
      </div>
      <div>
        <button @click="changeParameter('random', 'none')">Random Avatar</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        avatarUrl: '/avatar',
      };
    },
    methods: {
      fetchAvatar(url) {
        fetch(url)
          .then(response => response.blob())
          .then(blob => {
            let objectURL = URL.createObjectURL(blob);
            this.avatarUrl = objectURL;
          });
      },
      generateAvatar() {
        this.fetchAvatar('/avatar');
      },
    //   generateReallyRandomAvatar() {
    //     this.fetchAvatar('/really_random_avatar');
    //   },
      generateAvatarFromUsername() {
        let username = prompt('Please enter your username', 'Username');
        if (username) {
          this.fetchAvatar(`/avatar/${username}`);
        }
      },
      changeParameter(param, direction) {
        this.fetchAvatar(`/avatar/update?param=${param}&direction=${direction}`);
      },
    },
    mounted() {
      this.generateAvatar();
    },
  };
  </script>
  
  <style scoped>
  /* Add your styles here */
  </style>
  