#include "displayy3.h"
#include "ui_displayy3.h"
#include <QListView>
#include <QListWidgetItem>
#include <QFile>
#include <QTextStream>

displayy3::displayy3(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::displayy3)
{
    ui->setupUi(this);

    QFile file("/home/rakesh/Qt/Reco/python/movielens_1m_uid_aplha");
                file.open(QIODevice::ReadOnly | QIODevice::Text);

                QString path;

                QTextStream in1(&file);
                path= in1.readLine();
                ui->Uidvalue->setText(path);
                path=in1.readLine();
                ui->alphavalue->setText(path);


                QFile file2("/home/rakesh/Qt/Reco/python/movielens_1m_egocentricReco.json");
                file2.open(QIODevice::ReadOnly| QIODevice::Text);

                QTextStream reader(&file2);
                QListWidget *list=new QListWidget();
                ui->scrollArea->setWidget(list);

                while(!reader.atEnd()){
                    QString item=reader.readLine();


                QListWidgetItem *t=new QListWidgetItem(item,list);





                }






                QFile file3("/home/rakesh/Qt/Reco/python/movielens_1m_collaborativeReco.json");
                file3.open(QIODevice::ReadOnly| QIODevice::Text);

                QTextStream reader1(&file3);
                QListWidget *list1=new QListWidget();
                ui->scrollArea_2->setWidget(list1);

                while(!reader1.atEnd()){
                    QString item1=reader1.readLine();


                QListWidgetItem *t1=new QListWidgetItem(item1,list1);




                }


                QFile file4("/home/rakesh/Qt/Reco/python/movielens_1m_combinedReco.json");
                file4.open(QIODevice::ReadOnly| QIODevice::Text);

                QTextStream reader2(&file4);
                QListWidget *list2=new QListWidget();
                ui->scrollArea_3->setWidget(list2);

                while(!reader2.atEnd()){
                    QString item2=reader2.readLine();


                QListWidgetItem *t2=new QListWidgetItem(item2,list2);




                }



}


displayy3::~displayy3()
{
    delete ui;
}
