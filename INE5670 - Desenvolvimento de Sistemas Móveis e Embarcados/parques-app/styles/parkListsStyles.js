import {StyleSheet} from 'react-native';

export default styles = StyleSheet.create({
  containerList: {
    flex: 1,
    padding: 10,
  },

  card: {
    flex: 1,
    flexDirection: 'row',
    padding: 15,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 3,
    },
    shadowOpacity: 0.3,
    shadowRadius: 4.65,
    elevation: 6,
    backgroundColor: 'white',
    justifyContent: 'space-between',
    alignItems: 'center', 
    marginBottom: 10,
  },

  textContainer: {
    flex: 1,
    marginLeft: 5,
  },

  textName: {
    margin: 5,
    fontSize: 20,
    color: 'black',
    fontWeight: 'bold',
  },

  textAddress: {
    fontSize: 16,
    margin: 5,
    color: 'black',
  },
  
  logoPark: {
    height: 70,
    width: 70,
  },

  favoriteButton: {
    marginLeft: 'auto',
    fontSize: 35,
    color: '#FFBF00',
  },

  favoriteButtonContainer: {
    marginLeft: 10, 
  },

  messageContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    position: 'relative',
    borderRadius: 10,
    paddingVertical: 12,
    paddingHorizontal: 24,
    margin: 50,
    marginTop: 70,
    opacity: 0.6,
    backgroundColor: 'black'
  },

  messageText: {
    color: 'white',
    fontSize: 16,
  },

  noFavorites: {
    color: 'black',
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
    padding: 10,
    
  },

})