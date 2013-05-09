#include "userproflisty2.h"
#include "ui_userproflisty2.h"
#include <QDebug>
userproflisty2::userproflisty2(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::userproflisty2)
{
    ui->setupUi(this);

    showproc=new QProcess();
    attri=new QProcess();
    connect(showproc,SIGNAL(finished(int)),this,SLOT(showcompleted()));
    connect(ui->attribute,SIGNAL(currentTextChanged(QString)),this,SLOT(atrichange()));
    connect(attri,SIGNAL(finished(int)),this,SLOT(attribchange()));

    connect(ui->Next,SIGNAL(clicked()),this,SLOT(nectclicked()));



    QFile file("/home/rakesh/Qt/Reco/python/movielens_1m_uid_aplha");
                file.open(QIODevice::ReadOnly | QIODevice::Text);

                QString path;

                QTextStream in1(&file);
                path= in1.readLine();
                ui->uidvalue->setText(path);


                QFile file1("/home/rakesh/Qt/Reco/filename.txt");
                file1.open(QIODevice::ReadOnly | QIODevice::Text);
                QTextStream in(&file1);

                QString item = in.readLine();



                QString param="python /home/rakesh/Qt/Reco/python/3_show_attrib.py "+item+" "+ui->uidvalue->text();
                if(item.length()>0)
                {
            qDebug()<<param;
                showproc->start(param);}
                else{

                }

}

userproflisty2::~userproflisty2()
{
    delete ui;
}

void userproflisty2::showcompleted()
{
    qDebug()<<"end";
    //movielens_1m_userAttribImportance.png
    QFile file("/home/rakesh/Qt/Reco/python/db.txt");
            file.open(QIODevice::ReadOnly | QIODevice::Text);

QString path;
            QTextStream in(&file);
            path= in.readLine();
            path=path+"/movielens_1m_userAttribImportance.png";
            qDebug()<<path;

            QPixmap pixmap(path);

            QSize size(ui->img1->width(),ui->img1->height());
            pixmap=pixmap.scaled(size);
            ui->img1->setPixmap(pixmap);


            qDebug()<<"attri closed";
    QFile file1("/home/rakesh/Qt/Reco/python/db.txt");
                file1.open(QIODevice::ReadOnly | QIODevice::Text);


                QTextStream in1(&file1);
                QString p= in1.readLine();
                p=p+"/movielens_1m_attributes.txt";
                QFile attribute(p);
                attribute.open(QIODevice::ReadOnly| QIODevice::Text);

                QTextStream reader(&attribute);
                ui->attribute->clear();
                while(!reader.atEnd()){
                    QString item=reader.readLine();
                    ui->attribute->addItem(item);
                }


}

void userproflisty2::atrichange()
{
    QFile file1("/home/rakesh/Qt/Reco/filename.txt");
       file1.open(QIODevice::ReadOnly | QIODevice::Text);
       QTextStream in1(&file1);

       QString item = in1.readLine();



       QString param="python /home/rakesh/Qt/Reco/python/3_show_value.py "+item+" "+ui->uidvalue->text()+ " "+ui->attribute->currentText();
       if(item.length()>0)
       {
   qDebug()<<param;
       attri->start(param);}
       else{

       }
}

void userproflisty2::attribchange()
{

    qDebug()<<"attri closed";
    QFile file("/home/rakesh/Qt/Reco/python/db.txt");
                file.open(QIODevice::ReadOnly | QIODevice::Text);


                QTextStream in(&file);
                QString p= in.readLine();
                p=p+"/movielens_1m_userValueImportance.png";

                QPixmap pix(p);
                QSize size(ui->img2->width(),ui->img2->height());
                pix=pix.scaled(size);
                ui->img2->setPixmap(pix);
}

void userproflisty2::nectclicked()
{
    emit movenext();
}


