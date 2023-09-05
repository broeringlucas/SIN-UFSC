import * as React from 'react';
import { Text, View, ActivityIndicator, ScrollView, FlatList, TouchableOpacity, Image } from 'react-native';
import {BACKGROUND_COLOR, HEADER_COLOR} from '../config.js';
import stylesButton from '../styles/buttonStyle';
import styles from '../styles/parkListsStyles';


export default class FavoriteParksScreen extends React.Component {
  static navigationOptions = {
    title: 'Favoritos',
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
    let favoritesArray = props.navigation.getParam('favoritesArray');
    this.state = {
      isLoading: true,
      favoriteParks: favoritesArray,
    };
  }

  componentDidMount() {
    const {navigation} = this.props;
  
    this.focusListener = navigation.addListener('didFocus', () => {
      const data = require('../parks.json')
      this.setState({
        isLoading: false,
        parks: data,
      });
    });
  }

  componentWillUnmount() {
    this.focusListener.remove()
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
        {this.state.favoriteParks.length === 0 && (
          <View>
            <Text style={styles.noFavorites}>Não possui favoritos!</Text>
          </View>
        )}
        <FlatList style={styles.containerList}
          data={this.state.favoriteParks}
          renderItem={({item}) =>
          <View>
            <TouchableOpacity onPress={ () => navigate('ParkDetails', {park: item})}>
              <View style={styles.card}>
                <Image style={styles.logoPark} source={{uri: item.logo}}/>

                <View style={styles.textContainer}>
                  <Text style={styles.textName}>{item.name}</Text>
                  <Text style={styles.textAddress}>{item.address.city} {item.address.UF}</Text>
                </View>
                <Text style={styles.favoriteButton}>★</Text>
              </View>
            </TouchableOpacity>
          </View>
          }
        />
        <View style={stylesButton.buttonContainer}>
          <TouchableOpacity style={stylesButton.button} onPress={() => navigate('ParksList')} activeOpacity={0.6}>
            <Text style={stylesButton.buttonText}>Voltar</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    );
  }
}