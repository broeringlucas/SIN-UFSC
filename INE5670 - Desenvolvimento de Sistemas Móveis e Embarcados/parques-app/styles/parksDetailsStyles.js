import {StyleSheet} from 'react-native';

export default styles = StyleSheet.create({
  container: {
    padding: 15,
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  name: {
    fontSize: 20,
    fontWeight: 'bold',
    height: 44,
  },
  address: {
    fontSize: 13,
  },
  contactDetails: {
    fontSize: 16,
    height: 44,
  },
  contactContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 15,
    backgroundColor:'#FFBF00',
    margin: 10,
    borderRadius: 10,
    paddingVertical: 12,
    paddingHorizontal: 24,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 3,
    },
    shadowOpacity: 0.3,
    shadowRadius: 4.65,
    elevation: 6,
  },
  socialsContainer: {
    flex: 1,
    flexDirection: 'row',
    marginBottom: 10,
  },
  imageContainer: {
    padding: 20,
  },
  image: {
    width: '100%',
    height: 200,
    marginBottom: 10,
    borderRadius: 10,
  },
  logo: {
    height: 125,
    width: 125,
  },
});