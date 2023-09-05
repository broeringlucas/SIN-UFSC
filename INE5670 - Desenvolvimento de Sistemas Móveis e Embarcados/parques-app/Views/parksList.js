import * as React from 'react';
import { Text, View, ActivityIndicator, ScrollView, FlatList, TouchableOpacity, Image, Modal } from 'react-native';
import {BACKGROUND_COLOR, HEADER_COLOR} from '../config.js';
import AsyncStorage from '@react-native-async-storage/async-storage';
import styles from '../styles/parkListsStyles';
import stylesButton from '../styles/buttonStyle';
import {PATH} from '../config';

export default class ParksListScreen extends React.Component {
  static navigationOptions = {
    title: 'Parques',
    headerStyle: {
      backgroundColor: HEADER_COLOR,
      borderBottomColor: HEADER_COLOR,
      borderBottomWidth: 3,
        shadowOffset: {
          width: 0,
          height: 3,
        },
        shadowOpacity: 0.3,
        shadowRadius: 4.65,
        elevation: 6,
        },
    headerTitleStyle: {
      fontSize: 18,
      color: 'white',
    },
    headerTintColor: 'white',
  };

  constructor(props) {
    super(props) 
    this.state = {
      isLoading: true,
      favoriteParks: [],
  };
  }

  componentDidMount() {
    const {navigation} = this.props;

    this.focusListener = navigation.addListener('didFocus', () => {
      const data = PATH

      this.setState({
        isLoading: false,
        showMessageAdded: false,
        showMessageRemoved: false,
        parks: data,
      });

      this.getValue()
    });
  }

  componentWillUnmount() {
    this.focusListener.remove()
  }

  toggleFavorite = (park) => {
  const { favoriteParks } = this.state;
  const isFavorite = favoriteParks.some(favorite => favorite.id === park.id);

    if (isFavorite) {
      const index = favoriteParks.findIndex(favorite => favorite.id === park.id);
      favoriteParks.splice(index, 1)
      console.log(index)
      AsyncStorage.setItem('favoriteParks', JSON.stringify(favoriteParks));
      this.setState({
        favoriteParks: [...favoriteParks],
        showMessageAdded: true,
      },
      () => {
        setTimeout(() => {
          this.setState({ showMessageAdded: false, });
        }, 700);
      });
    } else {
      const list = favoriteParks.push(park)
      AsyncStorage.setItem('favoriteParks', JSON.stringify(favoriteParks));
      this.setState({
        favoriteParks: [...favoriteParks],
        showMessageRemoved: true,
      },
      () => {
        setTimeout(() => {
          this.setState({ showMessageRemoved: false });
        }, 700);
      });
    }
  };

  getValue = async () => {
      try {
        const storedFavorites = await AsyncStorage.getItem('favoriteParks');
        if (storedFavorites !== null) {
          const favoriteParks = JSON.parse(storedFavorites);
          console.log(favoriteParks.index)
          this.setState({ favoriteParks });
        }
      } catch (error) {
        console.error('Error retrieving favorite parks:', error);
      }
    }
    
  render() {
    if(this.state.isLoading){
      return(
        <View style={{flex: 1, padding: 20}}>
          <ActivityIndicator/>
        </View>
      )
    }

    const {navigate} = this.props.navigation;
    return(
      <ScrollView style={{backgroundColor: BACKGROUND_COLOR}}>
        <View>
          <Modal 
            animationType="fade"
            transparent={true}
            visible= {this.state.showMessageAdded || this.state.showMessageRemoved}
            style={styles.messageContainer}>
            {this.state.showMessageAdded && (
            <View style={styles.messageContainer}>
              <Text style={styles.messageText}>Removido aos favoritos!</Text>
            </View>)}
            
            {this.state.showMessageRemoved && (
            <View style={styles.messageContainer}>
              <Text style={styles.messageText}>Adicionado aos favoritos!</Text>
            </View>)}
          </Modal>
        </View>
        <FlatList style={styles.containerList}
          data={this.state.parks}
          renderItem={({item}) =>
          <View>
            <TouchableOpacity onPress={ () => navigate('ParkDetails', {park: item})}>
              <View style={styles.card}>
                <Image style={styles.logoPark} source={{uri: item.logo}}/>

                <View style={styles.textContainer}>
                  <Text style={styles.textName}>{item.name}</Text>
                  <Text style={styles.textAddress}>{item.address.city} {item.address.UF}</Text>
                </View>
                <TouchableOpacity onPress={() => this.toggleFavorite(item)} >
                  {this.state.favoriteParks.some(favorite => favorite.id === item.id) ? (
                    <Text style={styles.favoriteButton}>★</Text>
                  ) : (
                    <Text style={styles.favoriteButton}>☆</Text>
                  )}
                </TouchableOpacity>
              </View>
            </TouchableOpacity>
          </View>
          }
        />
        <View style={stylesButton.buttonContainer}>
          <TouchableOpacity style={stylesButton.button} onPress={ () => navigate('FavoriteParks', {favoritesArray: this.state.favoriteParks})} activeOpacity={0.6}>
            <Text style={stylesButton.buttonText}>Favoritos</Text>
          </TouchableOpacity>
        </View>
        <View style={stylesButton.buttonContainer}>
          <TouchableOpacity style={stylesButton.button} onPress={() => navigate('Home')} activeOpacity={0.6}>
            <Text style={stylesButton.buttonText}>Voltar</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    );
  }
}

