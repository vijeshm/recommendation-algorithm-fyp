#include "recommend.h"
#include "ui_recommend.h"
#include <QFile>
#include <QTextStream>
#include <QDebug>
#include <QString>
#include <QListWidget>
#include <QListWidgetItem>

recommend::recommend(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::recommend)
{
    ui->setupUi(this);
    proc=new QProcess();
    ythis=new QProcess();
    value="0";
    whythiswin=new whythiswindow();
    connect(ui->back,SIGNAL(clicked()),this,SLOT(moveback()));
    connect(ui->whythis,SIGNAL(clicked()),this,SLOT(openwindow()));
    connect(ui->alphaslider,SIGNAL(sliderMoved(int)),this,SLOT(alphachange()));
    connect(ui->show,SIGNAL(clicked()),this,SLOT(recomm()));
    connect(proc,SIGNAL(finished(int)),this,SLOT(proccompleted()));
    connect(ythis,SIGNAL(finished(int)),this,SLOT(ythisended()));


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

recommend::~recommend()
{
    delete ui;
}

void recommend::moveback()
{
    emit movebacktoclusterusers();
}


void recommend::openwindow()
{
    QFile file1("/home/rakesh/Qt/Reco/filename.txt");
        file1.open(QIODevice::ReadOnly | QIODevice::Text);
        QTextStream in1(&file1);

        QString item = in1.readLine();
        item=item+"_uid_aplha";

        QFile file(item);
        file.open(QIODevice::WriteOnly | QIODevice::Text);
        QTextStream out(&file);
        out << ui->userid->currentText();
        out<<"\n";
        out<<(ui->alphaslider->value()/100.0);
        file.close();


        QFile file3("/home/rakesh/Qt/Reco/python/db.txt");
                    file3.open(QIODevice::ReadOnly | QIODevice::Text);

                    QString path3;
                    QTextStream in(&file3);
                    path3= in.readLine();


                    QFile file4("/home/rakesh/Qt/Reco/filename.txt");
                        file4.open(QIODevice::ReadOnly | QIODevice::Text);
                        QTextStream in2(&file4);

                        QString item1 = in2.readLine();



                        path3="python "+path3+"/8_listMovie.py "+item1+ " "+ui->userid->currentText();
                    qDebug()<<path3;
                    ythis->start(path3);


ui->statuscontent->setWidget(new QLabel("running...please wait"));





}

void recommend::alphachange()
{
    int64_t val=ui->alphaslider->value();
    double v=val/100.0;
    value=QString::number(v);
    ui->alphavalue->setText(value);
}

void recommend::recomm()
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


                    path="python "+path+"/7_recommendItems.py "+item+" "+ui->userid->currentText() +" "+value;
                qDebug()<<path;
                proc->start(path);
                ui->statuscontent->setWidget(new QLabel("running"));


}

void recommend::proccompleted()
{
 ui->statuscontent->setWidget(new QLabel("completed"));

 QFile file("/home/rakesh/Qt/Reco/python/db.txt");
             file.open(QIODevice::ReadOnly | QIODevice::Text);

             QString path;

             QTextStream in1(&file);
             path= in1.readLine();
             path=path+"/movielens_1m_combinedReco.json";
             qDebug()<<path;
             QFile fileopen(path);
             fileopen.open(QIODevice::ReadOnly | QIODevice::Text);
             QTextStream in(&fileopen);
             QListWidget *list=new QListWidget();
             ui->contentscroll->setWidget(list);
             while(!in.atEnd())   {
             QString item = in.readLine();

             item=item.left(item.lastIndexOf(" "));
             QListWidgetItem *t=new QListWidgetItem(item,list);

             qDebug()<<item;



             }
}

void recommend::ythisended()
{
    ui->statuscontent->setWidget(new QLabel("ended"));
     whythiswin->show();
}
