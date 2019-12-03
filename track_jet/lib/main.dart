
import 'dart:async';
import 'package:flutter/services.dart';

import 'package:flutter/material.dart';
import './homeScreen.dart';

void main() {
  runApp(new MaterialApp(
    home: new SplashScreen(),
    routes: <String, WidgetBuilder>{
      '/HomeScreen': (BuildContext context) => new MyApp()
    },
  ));
}

class SplashScreen extends StatefulWidget {
  @override
  _SplashScreenState createState() => new _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  startTime() async {
    var _duration = new Duration(seconds: 2);
    return new Timer(_duration, navigationPage);
  }

  void navigationPage() {
    Navigator.of(context).pushReplacementNamed('/HomeScreen');
  }

  @override
  void initState() {
    super.initState();
    startTime();
  }

  @override
  /*Widget build(BuildContext context) {
    return new Scaffold(
      body: new Center(
        child: new Image.asset('assets/images/logo.jpg'),
      ),
    );
  }
}*/
Widget build(BuildContext context) {

    // To make this screen full screen.
    // It will hide status bar and notch.
SystemChrome.setEnabledSystemUIOverlays([]);

    // full screen image for splash screen.
  return Container(
    width:double.infinity,
    child: new Image.asset('assets/images/logo.jpg'));
  }
}
