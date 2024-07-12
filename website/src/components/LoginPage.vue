<template>
  <div class="wrapper">
    <form action="">
      <h1>Login</h1>
      <div class="input-box">
        <input type="text" placeholder="Username" required />
        <i class="bx bxs-user"></i>
      </div>
      <div class="input-box">
        <input type="password" placeholder="Password" required />
        <i class="bx bxs-lock-alt"></i>
      </div>
      <div class="remember-forgot">
        <label>
          <input type="checkbox" />Remember me
        </label>
        <a href="#">Forgot Password</a>
      </div>
      <button type="submit" @click="GoToTest" class="btn">Login</button>
      <div class="register-link">
        <p>Don't have an account? <a href="#">Register Here</a></p>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  methods: {
    GoToTest() {
      this.$router.push('/personal-test');
    }
  }
}
</script>

<style>


.wrapper {
  background: url('../assets/img.jpg') no-repeat;
  background-size: cover;
  background-position: center;
  width: 420px;
    background: transparent;
    border: 2px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(40px);
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    padding: 30px 40px;
}

.wrapper h1 {
  font-size: 36px;
  text-align: center;
}

.wrapper .input-box {
    width: 100%;
    height : 50px;
    margin : 30px 0;
}

.input-box input {
    width: 100%;
    height: 100%;
    background: transparent;
    border: none;
    outline: none;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 40px;
    font-size: 16px;
    padding: 20px 45px 20px 20px;
}

.input-box i {
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 20px;
}

.wrapper .remember-forgot {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    margin: 15px 0 15;
}

.remember-forgot label input {
    accent-color: #fff;
    margin-right: 3px;
}

.remember-forgot a {
    text-decoration: none;
}

.remember-forgot a:hover {
    text-decoration: underline;
}

.wrapper .btn {
    width : 100%;
    height : 50px;
    background: #fff;
    border: none;
    outline: none;
    border-radius: 40px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    font-size: 16px;
    color: #333;
    font-weight: 600;
    margin: 20px 0;
}

.wrapper .register-link {
    font-size: 14.5px;
    text-align: center;
    margin: 20px 0 15px;
}

.register-link p a {
    text-decoration: none;
    font-weight: 600;
}

.register-link p a:hover {
    text-decoration: underline;
}
</style>
