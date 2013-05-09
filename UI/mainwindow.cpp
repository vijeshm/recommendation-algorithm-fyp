#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    stackedWidget = new QStackedWidget;
    fw=new FirstWindow();
    up=new upload();
    userpro=new userprofile();
    reducedim =new reduceDimension();
    computesimi=new computesimilarity();
    clusteruser=new clusterusers();
    reco=new recommend();

    ui->setupUi(this);

     stackedWidget->addWidget(fw);
     stackedWidget->addWidget(up);
     stackedWidget->addWidget(userpro);
     stackedWidget->addWidget(reducedim);
     stackedWidget->addWidget(computesimi);
     stackedWidget->addWidget(clusteruser);
     stackedWidget->addWidget(reco);

    this->setCentralWidget(stackedWidget);
    connect(fw,SIGNAL(movenext()),this,SLOT(movesecond()));
    connect(up,SIGNAL(movenext()),this,SLOT(moveuserprofile()));
    connect(userpro,SIGNAL(moverecucedimension()),this,SLOT(movereducedim()));
    connect(reducedim,SIGNAL(movetocomputesimilarity()),this,SLOT(movetocomputesimilarity()));
    connect(computesimi,SIGNAL(movetoclusterusers()),this,SLOT(movetoclusteruser()));
    connect(clusteruser,SIGNAL(movetorecommend()),this,SLOT(movetorecommend()));

    connect(userpro,SIGNAL(movebacktoupload()),this,SLOT(movebacktoupload()));
    connect(reducedim,SIGNAL(movebacktouserprofile()),this,SLOT(movebacktouserprofile()));
    connect(computesimi,SIGNAL(movebacktoreducedimension()),this,SLOT(movebacktoreducedimension()));
    connect(clusteruser,SIGNAL(movebacktocommputesimilarity()),this,SLOT(movebacktocomputesimilarity()));
    connect(reco,SIGNAL(movebacktoclusterusers()),this,SLOT(movebacktoclusterusers()));

}

MainWindow::~MainWindow()
{

    delete ui;
}

void MainWindow::movesecond()
{this->stackedWidget->setCurrentIndex(1);
}

void MainWindow::moveuserprofile()
{
    this->stackedWidget->setCurrentIndex(2);
}

void MainWindow::movereducedim()
{
    this->stackedWidget->setCurrentIndex(3);
}

void MainWindow::movetocomputesimilarity()
{
    this->stackedWidget->setCurrentIndex(4);
}

void MainWindow::movetoclusteruser()
{

    this->stackedWidget->setCurrentIndex(5);
}

void MainWindow::movetorecommend()
{
    this->stackedWidget->setCurrentIndex(6);
}

void MainWindow::movebacktoupload()
{

  this->stackedWidget->setCurrentIndex(1);
}

void MainWindow::movebacktouserprofile()
{

    this->stackedWidget->setCurrentIndex(2);
}

void MainWindow::movebacktoreducedimension()
{
    this->stackedWidget->setCurrentIndex(3);
}

void MainWindow::movebacktocomputesimilarity()
{this->stackedWidget->setCurrentIndex(4);
}

void MainWindow::movebacktoclusterusers()
{
    qDebug()<<"here";
    this->stackedWidget->setCurrentIndex(5);
}

