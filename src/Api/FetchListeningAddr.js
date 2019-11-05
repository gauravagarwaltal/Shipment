import { Users } from "../mockData/mockUsers";

async function FetchListeningAddr(pub_addr) {

    Users.map(each => {
        if (each.address === pub_addr) {
            // console.log(each)
            return each.listen
        }
    })
    return null
}

export default FetchListeningAddr; 