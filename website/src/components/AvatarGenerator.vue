<template>
  <div>
    <h1>Random Avatar Generator</h1>
    <div id="avatar">
      <img :src="avatarUrl" alt="Avatar" id="avatar-image" />
    </div>
    <div>
      <button @click="changeParameter('dec', 'styles')">Previous Style</button>
      <button @click="changeParameter('inc', 'styles')">Next Style</button>
    </div>
    <div>
      <button @click="changeParameter('dec', 'background_colors')">
        Previous Background Color
      </button>
      <button @click="changeParameter('inc', 'background_colors')">
        Next Background Color
      </button>
    </div>
    <div>
      <button @click="changeParameter('dec', 'hairstyles')">
        Previous Hairstyle
      </button>
      <button @click="changeParameter('inc', 'hairstyles')">
        Next Hairstyle
      </button>
    </div>
    <div>
      <button @click="changeParameter('dec', 'clothing_color')">
        Previous Clothing Color
      </button>
      <button @click="changeParameter('inc', 'clothing_color')">
        Next Clothing Color
      </button>
    </div>
    <div>
      <button @click="changeParameter('dec', 'eyebrows')">
        Previous Eyebrows
      </button>
      <button @click="changeParameter('inc', 'eyebrows')">Next Eyebrows</button>
    </div>
    <div>
      <button @click="changeParameter('dec', 'eyes')">Previous Eyes</button>
      <button @click="changeParameter('inc', 'eyes')">Next Eyes</button>
    </div>
    <div>
      <button @click="changeParameter('dec', 'nose')">Previous Nose</button>
      <button @click="changeParameter('inc', 'nose')">Next Nose</button>
    </div>
    <div>
      <button @click="changeParameter('dec', 'mouth')">Previous Mouth</button>
      <button @click="changeParameter('inc', 'mouth')">Next Mouth</button>
    </div>
    <div>
      <button @click="changeParameter('dec', 'facial_hair')">
        Previous Facial Hair
      </button>
      <button @click="changeParameter('inc', 'facial_hair')">
        Next Facial Hair
      </button>
    </div>
    <div>
      <button @click="changeParameter('dec', 'skin_color')">
        Previous Skin Color
      </button>
      <button @click="changeParameter('inc', 'skin_color')">
        Next Skin Color
      </button>
    </div>
    <div>
      <button @click="changeParameter('dec', 'hair_color')">
        Previous Hair Color
      </button>
      <button @click="changeParameter('inc', 'hair_color')">
        Next Hair Color
      </button>
    </div>
    <div>
      <button @click="changeParameter('dec', 'accessory')">
        Previous Accessory
      </button>
      <button @click="changeParameter('inc', 'accessory')">
        Next Accessory
      </button>
    </div>
    <div>
      <button @click="changeParameter('dec', 'clothing_types')">
        Previous Clothing
      </button>
      <button @click="changeParameter('inc', 'clothing_types')">
        Next Clothing
      </button>
    </div>
    <div>
      <button @click="changeParameter('inc', 'clothing_graphics')">
        Previous Clothing Graphics
      </button>
      <button @click="changeParameter('dec', 'clothing_graphics')">
        Next Clothing Graphics
      </button>
    </div>
    <div>
      <button @click="generateAvatar">Random Avatar</button>
    </div>
    <div>
      <button @click="go_to_index">Start</button>
    </div>
  </div>
</template>

<script>
const serverUrl = "http://localhost:5000";
export default {
  data() {
    return {
      avatarUrl: "/avatar",
    };
  },
  methods: {
    fetchAvatar(url) {
      console.log(
        `Url: ${url} index_dict: ${sessionStorage.getItem("index-dict")}`
      );
      fetch(url, {
        headers: {
          "Content-Type": "application/json",
          "index-dict": sessionStorage.getItem("index-dict") || "test",
        },
      })
        .then((response) => {
          if (!response.ok) {
            return response.json().then((error) => {
              throw new Error(error.error);
            });
          }
          // Store the header called Index_dict into sessionStorage, it must overwrite the previous one
          let Index_dict = response.headers.get("index-dict");
          console.log(Index_dict);
          sessionStorage.setItem("index-dict", Index_dict);
          return response.blob();
        })
        .then((blob) => {
          let objectURL = URL.createObjectURL(blob);
          this.avatarUrl = objectURL;
        })
        .catch((error) => {
          alert(error);
        });
    },
    go_to_index() {
      this.$router.push("/StartButton");
    },
    generateAvatar() {
      this.fetchAvatar(serverUrl + "/avatar/random");
    },
    //   generateReallyRandomAvatar() {
    //     this.fetchAvatar('/really_random_avatar');
    //   },
    generateAvatarFromUsername() {
      let username = prompt("Please enter your username", "Username");
      if (username) {
        this.fetchAvatar(serverUrl + "/avatar/" + username);
      }
    },
    changeParameter(action, attr) {
      this.fetchAvatar(serverUrl + `/avatar/regenerate/${action}/${attr}`);
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
