<template>
	<div>
		<h3> Test </h3>

		<form @submit.prevent="searchQuery">
			<input 
			   name="searchQuery" type="text" v-model="query"
			   placeholder="Search something"
			>
			<button type="submit">Search</button>
		</form>

		<div class="tweet" v-for="(tweet, key) in tweets" :key="key" v-if="tweets.length > 0">
			<div class="tweet__container">
				{{ tweet }}	
			</div>
		</div>
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
	background-color: #ccc;
	box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
	border-radius: 5px;

	&__container {
		padding: 2px 16px;
	}

	&:hover {
		box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
	}
}
</style>
