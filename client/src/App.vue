<template>
	<div id="main-div">
		<header>
			<h2> TF-IDF indexed tweet searcher </h2>
		</header>

		<div id="main-content">
			<form @submit.prevent="searchQuery">
				<input 
					 id="search-bar" name="searchQuery" type="text" v-model="query"
					 placeholder="Search something"
				>
			</form>

			<div class="tweet" v-for="(tweet, key) in tweets" :key="key" v-if="tweets.length > 0">
				<div class="tweet__container">
					{{ tweet.text }}	
				</div>
			</div>
		</div>

		<footer>
			<a href="https://www.utec.edu.pe/"><img src="../src/assets/utec_logo.png"></a>
			<div id="github-links"> 
				<a href=""> Piero Marini Monsante </a>
				<a href=""> | Gonzalo Alfaro Caso </a>
			</div>
		</footer>

	</div>
</template>

<script>
export default {
	name: 'App',
	data() {
		return {
			tweets: [],
			query: ''
		}
	},
	methods: {
		searchQuery() {
			this.$http.post('http://localhost:5000/search', { 'query': this.query })
				.then(res => {
					this.tweets = res.data.tweets
				})
				.catch(err => {
					console.error(err)
				})
		}
	}
}
</script>

<style lang="scss" scoped>

#main-div {
	width: 100%;
	height: 100vh;
	font-family: 'Roboto', "sans-serif";
}

header {
	width: 100%;
	height: 8%;
	background-color: #2b2b2b;
	color: white;
	padding: 10px;
}

#main-content {
	width: 60%;
	height: 60%;
	margin: 5% auto;
}

form {
	margin: 40px 0;
	width: 100%;
	text-align: center;
}

#search-bar {
	width: 100%;
	height: 40px;
}

footer {
	width: 100%;
	height: 8%;
	background-color: #2b2b2b;
	color: white;
}

img {
	width: 100px;
	margin: 10px 10px;
}

a {
	color: white;
	text-decoration: none;
}

#github-links {
	width: 50%;
	float: right;
	text-align: right;
	margin: 25px;
}

#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
	margin-top: 60px;
}
.tweet {
	display: flex;
	text-align: center;
	background-color: #eee;
	box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
	border-radius: 5px;
	font-size: 100%;
	margin: 25px 0;
	width: 100%;

	&__container {
		padding: 8px 16px;
	}

	&:hover {
		box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
	}
}
</style>
