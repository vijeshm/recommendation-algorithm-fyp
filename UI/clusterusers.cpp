#include "clusterusers.h"
#include "ui_clusterusers.h"
#include <QDebug>
#include <QFile>
#include <QTextStream>
#include <QListWidget>
#include <QListWidgetItem>

clusterusers::clusterusers(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::clusterusers)
{
    ui->setupUi(this);
    proc=new QProcess();
    showproc=new QProcess();
    connect(ui->next,SIGNAL(clicked()),this,SLOT(movenext()));
    connect(ui->back,SIGNAL(clicked()),this,SLOT(moveback()));
    connect(ui->clusteruser,SIGNAL(clicked()),this,SLOT(clusterclick()));
    connect(ui->show,SIGNAL(clicked()),this,SLOT(showclick()));
    connect(proc,SIGNAL(finished(int)),this,SLOT(clusterended()));
    connect(showproc,SIGNAL(finished(int)),this,SLOT(showprocended()));




    QFile file("/home/rakesh/Qt/Reco/python/db.txt");
                file.open(QIODevice::ReadOnly | QIODevice::Text);

                QString path;

                QTextStream in1(&file);
                path= in1.readLine();
                path=path+"/movielens_1m_userlist.json";
                qDebug()<<path;
                QFile fileopen(path);
                fileopen.open(QIODevice::ReadOnly | QIODevice::Text);
                QTextStream in(&fileopen);
                ui->userid->clear();
                while(!in.atEnd())   {
                QString item = in.readLine();
                ui->userid->addItem(item);
                qDebug()<<item;



}
}

clusterusers::~clusterusers()
{
    delete ui;
}

void clusterusers::movenext()
{

    emit movetorecommend();
}

void clusterusers::moveback()
{
    emit movebacktocommputesimilarity();
}

void clusterusers::clusterclick()
{

    QFile file("/home/rakesh/Qt/Reco/python/db.txt");
                file.open(QIODevice::ReadOnly | QIODevice::Text);

                QString path;
                QTextStream in(&file);
                path= in.readLine();


                QFile file1("/home/rakesh/Qt/Reco/filename.txt");
                    file1.open(QIODevice::ReadOnly | QIODevice::Text);
                    QTextStream in1(&file1);

                    QString item = in1.readLine();


                path="python "+path+"/6_clusterUsers.py "+item;
                qDebug()<<path;
                proc->start(path);

                ui->status_scrollarea->setWidget(new QLabel("running..."));


}

void clusterusers::showclick()
{
    QFile file("/home/rakesh/Qt/Reco/python/db.txt");
                file.open(QIODevice::ReadOnly | QIODevice::Text);

                QString path;
                QTextStream in(&file);
                path= in.readLine();


                QFile file1("/home/rakesh/Qt/Reco/filename.txt");
                    file1.open(QIODevice::ReadOnly | QIODevice::Text);
                    QTextStream in1(&file1);

                    QString item = in1.readLine();


                    path="python "+path+"/6_userCluster.py "+item+" "+ui->userid->currentText();
                qDebug()<<path;
                showproc->start(path);

                ui->status_scrollarea->setWidget(new QLabel("running..."));
}

void clusterusers::showprocended()
{
                 ui->status_scrollarea->setWidget(new QLabel("ended"));
                 QFile file("/home/rakesh/Qt/Reco/python/db.txt");
                             file.open(QIODevice::ReadOnly | QIODevice::Text);

                             QString path;

                             QTextStream in1(&file);
                             path= in1.readLine();
                             path=path+"/movielens_1m_userClusters.json";
                             qDebug()<<path;
                             QFile fileopen(path);
                             fileopen.open(QIODevice::ReadOnly | QIODevice::Text);
                             QTextStream in(&fileopen);
                             QListWidget *list=new QListWidget();
                             ui->scrollArea->setWidget(list);
                             while(!in.atEnd())   {
                             QString item = in.readLine();
                             QListWidgetItem *t=new QListWidgetItem(item,list);

                             qDebug()<<item;



             }


}

void clusterusers::clusterended()
{
    ui->status_scrollarea->setWidget(new QLabel("completed...press show to display image"));
}
