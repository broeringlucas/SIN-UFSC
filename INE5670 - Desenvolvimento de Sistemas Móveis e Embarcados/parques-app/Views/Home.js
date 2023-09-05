 import * as React from 'react';
import {View, Text, Image, BackHandler,TouchableOpacity, ScrollView} from 'react-native';
import {BACKGROUND_COLOR, HEADER_COLOR} from '../config';
import styles from '../styles/homeStyles';
import stylesButton from '../styles/buttonStyle';

export default class HomeScreen extends React.Component {
  static navigationOptions = {
    title: 'Home',
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
      alignSelf: 'center'
    },
  };

  render() {
    const {navigate} = this.props.navigation;
    return (
      <ScrollView style={{backgroundColor: BACKGROUND_COLOR}}>
        <View style={styles.containerHome}>
          <Image style={styles.logo} source={require('../assets/roller-coaster.png')} />

          <Text style={styles.title}> Park Finder</Text>
          <Text style={styles.subtitle}> Where Adventures Begin</Text>
        </View>
        <View style={{transform: 'translateY(85%)'}}>
          <View style={stylesButton.buttonContainer}>
            <TouchableOpacity style={stylesButton.button} onPress={() => navigate('ParksList')} activeOpacity={0.6}>
              <Text style={stylesButton.buttonText}>Ver Parques</Text>
            </TouchableOpacity>
          </View>
          <View style={stylesButton.buttonContainer}>
            <TouchableOpacity style={stylesButton.button} onPress={() => BackHandler.exitApp()} activeOpacity={0.6}>
              <Text style={stylesButton.buttonText}>Sair</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    );
  }
}

