const fetchLastState = async (channelId) => {
    try {
        console.log(localStorage.getItem(channelId))
    } catch (error) {
        console.log("contract details are tempered or connectivity issue")
        console.log(error)
    }
}



export { fetchLastState };