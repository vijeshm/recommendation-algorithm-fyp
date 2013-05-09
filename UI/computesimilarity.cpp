#include "computesimilarity.h"
#include "ui_computesimilarity.h"
#include <QDebug>
#include <QFile>
#include <QTextStream>
#include<QPixmap>
#include <QSize>

computesimilarity::computesimilarity(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::computesimilarity)
{
    ui->setupUi(this);
    proc=new QProcess();
    showproc=new QProcess();
    connect(ui->back,SIGNAL(clicked()),this,SLOT(moveback()));
    connect(ui->next,SIGNAL(clicked()),this,SLOT(movenext()));
    connect(ui->computesimilarity_2,SIGNAL(clicked()),this,SLOT(computesimilarityslot()));
    connect(proc,SIGNAL(finished(int)),this,SLOT(computeover()));
    connect(showproc,SIGNAL(finished(int)),this,SLOT(showover()));
    connect(ui->show,SIGNAL(clicked()),this,SLOT(showclick()));
    connect(ui->zoom,SIGNAL(clicked()),this,SLOT(zoom()));

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

computesimilarity::~computesimilarity()
{
    delete ui;
}

void computesimilarity::movenext()
{
    qDebug()<<"click";
    emit movetoclusterusers();
}

void computesimilarity::moveback()
{
    emit movebacktoreducedimension();
}

void computesimilarity::computesimilarityslot()
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


                path="python "+path+"/5_computeSimilarity.py "+item;
                qDebug()<<path;
                proc->start(path);

                ui->scrollArea->setWidget(new QLabel("running..."));



}

void computesimilarity::computeover()
{

    ui->scrollArea->setWidget(new QLabel("completed.press show"));
}

void computesimilarity::showover()
{QFile file("/home/rakesh/Qt/Reco/python/db.txt");
    file.open(QIODevice::ReadOnly | QIODevice::Text);

QString path;
    QTextStream in(&file);
    path= in.readLine();
    path=path+"/movielens_1m_userSimilarity.png";



    QPixmap p(path);
    QSize size(ui->img->width(),ui->img->height());
    p=p.scaled(size);
    ui->img->setPixmap(p);

}

void computesimilarity::showclick()
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


                    path="python "+path+"/5_userSimilarity.py "+item+" "+ui->userid->currentText();
                qDebug()<<path;
                showproc->start(path);

                ui->scrollArea->setWidget(new QLabel("running..."));

}

void computesimilarity::zoom()
{
    QFile file("/home/rakesh/Qt/Reco/python/db.txt");
        file.open(QIODevice::ReadOnly | QIODevice::Text);

    QString path;
        QTextStream in(&file);
        path= in.readLine();
        path=path+"/movielens_1m_userSimilarity.png";

        QProcess *p=new QProcess();
        path="shotwell "+path;
        p->start(path);
}
