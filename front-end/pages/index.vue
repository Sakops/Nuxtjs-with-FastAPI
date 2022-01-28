<template>
  <div>
    <div>
      <div class="card" v-for="user in users" :key="user.id">

        <p>id: {{ user.id }}</p>
        <p>name: {{ user.first_name }}</p>
        <p>salary: {{ user.salary }}</p>
        <p>photo_url: {{ user.image }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="js">
import axios from "axios";
export default {
  data() {
    return {
      users: [],
      num: 0
    }
  },
  async mounted(){
    const {data} = await axios.get("http://127.0.0.1:8000/api/users")
    this.users = data;
  },
  methods:{
    add(){
      this.num += 1;
    },
    minus(){
      this.num -= 1;
    }
  }

}
</script>

<style scoped>
  .card{
    display: inline-block;
    width: 400px;
    margin: 2rem;
    align-items: center;
    border-radius: 10px;
    background-color: rgb(50, 27, 155);
  }

  .users{
    display: grid; 
    grid-template-columns: 1fr 1fr 1fr 1fr;
    margin: 2rem;
    padding: 1.5rem;
    color: white;
  }
  .users img{
    width: 150px;
    padding-left: 1rem;
  }
  .user p{
    display: inline-block;
  }
</style>