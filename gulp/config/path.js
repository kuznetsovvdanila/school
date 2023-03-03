import gulp from 'gulp';
import * as nodePath from 'path';

const rootdir = nodePath.basename(nodePath.resolve())
const appdir = 'school_app'
const staticdir = 'static'

export const path = {
    html : {
        dest : `../${rootdir}/${appdir}/templates/`,
        files : `../${rootdir}/${appdir}/templates/**/*.html`,
    },
    css : {
        dest : `../${rootdir}/${appdir}/${staticdir}/css/`,
        files : `../${rootdir}/${appdir}/${staticdir}/css/**/*.css`,
    },
    js : {
        dest : `../${rootdir}/${appdir}/${staticdir}/js/`,
        files : `../${rootdir}/${appdir}/${staticdir}/js/**/*.js`,
    },
    sass : {
        dest : `../${rootdir}/${appdir}/${staticdir}/sass/`,
        files : `../${rootdir}/${appdir}/${staticdir}/sass/**/*.sass`,
    },
};