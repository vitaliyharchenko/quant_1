'use strict';

//http://www.codevoila.com/post/32/customize-bootstrap-using-bootstrap-sass-and-gulp

var
    gulp = require('gulp'),
    sass = require('gulp-sass'),
    uglify = require('gulp-uglify'),
    clean = require('gulp-clean'),
    imagemin = require('gulp-imagemin'),
    rigger = require('gulp-rigger');

// source and distribution folder
var
    source = 'quantzone/src/',
    dest = 'quantzone/assets/';

// Bootstrap scss source
var bootstrapSass = {
        in: './node_modules/bootstrap/'
    };

// Bootstrap fonts source
var fonts = {
        in: [source + 'fonts/*.*', bootstrapSass.in + 'assets/fonts/**/*'],
        out: dest + 'fonts/'
    };

// Our scss source folder: .scss files
var scss = {
    in: source + 'scss/main.scss',
    out: dest + 'css/',
    watch: source + 'scss/**/*',
    clean: dest + 'css/',
    sassOpts: {
        outputStyle: 'nested',
        precison: 3,
        errLogToConsole: true,
        includePaths: [bootstrapSass.in + 'scss']
    }
};

// Our js source folder: .js files
var js = {
    in: source + 'js/main.js',
    out: dest + 'js/',
    watch: source + 'js/**/*',
    clean: dest + 'js/'
};

var img = {
    in: source + 'images/**/*',
    out: dest + 'images/',
    watch: source + 'images/**/*',
    clean: dest + 'images/'
};

// copy bootstrap required fonts to dest
gulp.task('fonts', function () {
    return gulp
        .src(fonts.in)
        .pipe(gulp.dest(fonts.out));
});

// compile scss
gulp.task('sass', function () {
    return gulp.src(scss.in)
        .pipe(sass(scss.sassOpts))
        .pipe(gulp.dest(scss.out));
});

// compile js
gulp.task('js', function () {
    return gulp.src(js.in)
        .pipe(rigger())
        .pipe(uglify())
        .pipe(gulp.dest(js.out));
});

// compile img
gulp.task('images', function () {
    return gulp.src(img.in)
        .pipe(imagemin())
        .pipe(gulp.dest(img.out));
});

// TODO: clear task

// default task
gulp.task('default', ['sass', 'js', 'images'], function () {
     gulp.watch(scss.watch, ['sass']);
     gulp.watch(js.watch, ['js']);
     gulp.watch(img.watch, ['images']);
});